import httpx
import json
import os
import time
from datetime import datetime, timedelta, timezone


def query_sumologic(
    query: str,
    from_time: str = None,
    to_time: str = None,
    max_results: int = 10_000,
) -> list[str]:
    """Query SumoLogic logs via Search Job API v2.

    Credentials and API endpoint are auto-configured from the agent's environment.

    Args:
        query: SumoLogic query string.
        from_time: Start time as ISO string (e.g., "2026-05-28T00:00:00Z"). Defaults to 1 hour ago.
        to_time: End time as ISO string. Defaults to now.
        max_results: Maximum messages to return.

    Returns:
        List of raw log strings from the _raw field.
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
    to_ms = int(now.timestamp() * 1000)

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

    return [m.get("_raw", "") for m in results]
