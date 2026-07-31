import httpx
import json
import os
import time
from datetime import datetime, timedelta, timezone


def query_sumologic(
    query: str,
    from_time: str = None,
    to_time: str = None,
    max_results: int = 1_000,
) -> dict:
    """Query SumoLogic logs via Search Job API v2.

    Credentials and API endpoint are auto-configured from the agent's environment.

    When the agent has a staging directory (LETTA_STAGING_DIR), full results are
    written to a file and a compact summary is returned. The agent can then use
    grep_files or file_read to search the full data. Without a staging directory,
    compact records are returned directly.

    Args:
        query: SumoLogic query string.
        from_time: Start time as ISO string (e.g., "2026-05-28T00:00:00Z"). Defaults to 1 hour ago.
        to_time: End time as ISO string. Defaults to now.
        max_results: Maximum messages to return. Default 1000.

    Returns:
        When staging is available: dict with summary (record_count, time_range,
        file_path, sample_records). When staging is not available: dict with
        compact_records (list of extracted key fields).
    """
    now = datetime.now(timezone.utc)

    if from_time:
        from_dt = datetime.fromisoformat(from_time.replace("Z", "+00:00"))
        if from_dt.tzinfo is None:
            from_dt = from_dt.replace(tzinfo=timezone.utc)
    else:
        from_dt = now - timedelta(hours=1)

    if to_time:
        to_dt = datetime.fromisoformat(to_time.replace("Z", "+00:00"))
        if to_dt.tzinfo is None:
            to_dt = to_dt.replace(tzinfo=timezone.utc)
    else:
        to_dt = now

    from_ms = int(from_dt.timestamp() * 1000)
    to_ms = int(to_dt.timestamp() * 1000)

    creds = json.loads(os.getenv("CREDENTIAL_SUMOLOGIC_KEYS"))
    access_id = creds.get("primary_key", "")
    access_key = creds.get("secondary_key", "")
    host = creds.get("url", "") or "https://api.sumologic.com/api"

    with httpx.Client(
        base_url=host,
        auth=(access_id, access_key),
        timeout=httpx.Timeout(120.0, connect=30.0),
        follow_redirects=True,
    ) as client:
        # Create job
        resp = client.post("/v2/search/jobs", json={"query": query, "from": from_ms, "to": to_ms, "timeZone": "UTC"})
        resp.raise_for_status()
        job_id = resp.json()["id"]

        try:
            # Poll for completion
            for _ in range(150):  # 5 min timeout at 2s intervals
                resp = client.get(f"/v2/search/jobs/{job_id}")
                resp.raise_for_status()
                state = resp.json().get("state", "")
                if state == "CANCELLED":
                    raise ValueError(f"Job {job_id} cancelled")
                if state.startswith("DONE"):
                    message_count = resp.json().get("messageCount", 0)
                    break
                time.sleep(2)
            else:
                raise TimeoutError(f"Job {job_id} timed out")

            # Fetch messages
            results = []
            offset = 0
            while offset < min(message_count, max_results):
                limit = min(10_000, max_results - offset)
                resp = client.get(f"/v2/search/jobs/{job_id}/messages", params={"offset": offset, "limit": limit})
                resp.raise_for_status()
                messages = resp.json().get("messages", [])
                if not messages:
                    break
                for msg in messages:
                    results.append(msg.get("map", msg))
                offset += len(messages)

        finally:
            # Clean up
            try:
                client.delete(f"/v2/search/jobs/{job_id}")
            except Exception:
                pass

    # Parse raw logs
    parsed_results = []
    for m in results:
        raw = m.get("_raw", "{}")
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            parsed = {"_raw": str(raw)[:500]}
        parsed_results.append(parsed)

    staging_dir = os.getenv("LETTA_STAGING_DIR")

    if staging_dir:
        # Write full results to staging directory
        out_dir = os.path.join(staging_dir, "sumologic")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "query_results.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed_results, f, indent=2, default=str)

        # Build compact summary for the tool return
        sample = _extract_compact(parsed_results[:3])
        return {
            "record_count": len(parsed_results),
            "time_range": {
                "from": from_dt.isoformat(),
                "to": to_dt.isoformat(),
            },
            "file_path": "sumologic/query_results.json",
            "sample_records": sample,
        }
    else:
        # No staging — return compact records directly
        return {"compact_records": _extract_compact(parsed_results)}


def _extract_compact(records: list[dict]) -> list[dict]:
    """Extract key security fields from parsed log records."""
    _keep_keys = {
        "event_id", "EventID", "event_type", "EventType",
        "level", "Level", "severity", "Severity",
        "source", "Source", "Provider", "provider",
        "message", "Message", "message_text",
        "computer", "ComputerName", "hostname", "Host",
        "user", "UserName", "User", "account", "SubjectUserName",
        "process", "ProcessName", "Image", "process_name",
        "pid", "ProcessId", "process_id",
        "command", "CommandLine", "command_line",
        "action", "Action", "action_type",
        "ip", "IpAddress", "SourceIp", "DestIp", "source_ip", "dest_ip",
        "port", "Port", "SourcePort", "DestPort",
        "protocol", "Protocol",
        "result", "Result", "status", "Status",
        "record_id", "RecordID",
    }
    _keep_lower = {k.lower() for k in _keep_keys}

    compact = []
    for parsed in records:
        record = {}

        # Extract timestamp
        for ts_key in ("@timestamp", "timestamp", "time", "TimeGenerated", "UtcTime"):
            val = parsed.get(ts_key)
            if val:
                record["timestamp"] = val
                break

        for k, v in parsed.items():
            if k in _keep_keys or k.lower() in _keep_lower:
                record[k] = v

        # Flatten nested event_id / execution / rendering_info
        for nested_key in ("event_id", "execution", "rendering_info"):
            nested = parsed.get(nested_key, {})
            if isinstance(nested, dict):
                for nk, nv in nested.items():
                    if nk in _keep_keys or nk.lower() in _keep_lower:
                        record[nk] = nv

        # If nothing was extracted, keep a truncated raw fallback
        if len(record) <= 1:
            record["_raw"] = str(parsed)[:500]

        compact.append(record)

    return compact
