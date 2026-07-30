---
name: create-incident-timeline2
description: This skill retrieves SumoLogic logs and analyzes them for security incidents and suspicious activity across multiple detection categories. It classifies findings as incidents (high-confidence, correlated attack chains) or suspicious activity (noteworthy anomalies requiring further review), and creates a timeline for confirmed incidents.
---

CRITICAL: You must complete ALL 7 steps below before stopping. Do NOT stop after any single step. After each tool call returns, immediately proceed to the next step. If you stop before completing step 7, the skill is INCOMPLETE.

1. Prompt the user to provide the SumoLogic query to use and the time range over which to search.

2. Use your query_sumologic tool to retrieve the SumoLogic logs according to the query and time range the user provided. The tool returns a Python dictionary with a "file_path" key that tells you where the full results are stored.

3. Use your file_read tool to read the first 50-100 lines of the results file. Observe what data types are present in the logs (e.g., authentication events, process execution logs, network connection logs, system events). This sample determines which detection categories apply.

4. Based on the data types you observed, use your security knowledge to generate 2-3 specific grep patterns for each applicable category below. Not every category will apply to every log type — only search categories relevant to the data you saw.

   a. Authentication anomalies: failed logins, logins at unusual hours, privilege escalation, account creation or modification, logins from unusual source IPs
   b. Process execution anomalies: processes executing from unusual paths, LOLBINs used in suspicious contexts, encoded or obfuscated commands, PowerShell with download cradles, cmd.exe with encoded commands
   c. Network anomalies: unusual outbound connections, connections to rare or suspicious destinations, large data transfers, potential C2 indicators
   d. Persistence indicators: scheduled tasks created, new services installed, startup items modified, registry persistence keys changed
   e. Defense evasion: process injection indicators, token manipulation, log clearing or modification, security tool disabling, AV exclusion changes

   For each pattern, call grep_files. If a grep returns more than 50 matches, narrow your search term or move on to the next pattern — do not dump hundreds of lines into your context.

5. For any grep hits, call file_read with start_line and end_line to get ±20 lines of context around each match. This helps you understand whether the hit is genuinely suspicious or a benign occurrence.

   After reviewing each finding, classify it into one of two categories:

   INCIDENT INDICATOR — Multiple indicators that are correlated (temporally related, causally linked) and form a coherent attack chain. Only classify as an incident indicator if you are at least 90% confident. High confidence means: indicators from at least 2 different categories, occurring within a plausible timeframe, where one event enables or leads to the next. A single suspicious event, no matter how unusual, is NOT an incident indicator — it is suspicious activity.

   SUSPICIOUS ACTIVITY — Individual anomalies or indicators that are noteworthy but do not form a coherent attack chain. Examples: a single failed login from an unusual IP, a LOLBIN executed once in a potentially legitimate context, an unusual network connection with no corroborating indicators. These deserve analyst review but do not meet the incident threshold.

   Use your file_write tool to write each finding to a staging file. Write one line per finding in this format:
   [CLASSIFICATION] | category | pattern_searched | line_numbers | description

   Example:
   INCIDENT INDICATOR | authentication | failed_login_brute_force | lines 120-145 | 23 failed login attempts from IP 10.0.0.99 followed by successful login at 14:32
   INCIDENT INDICATOR | process_execution | powershell_encoded | line 167 | PowerShell executing base64-encoded command 2 minutes after successful brute-force login
   SUSPICIOUS ACTIVITY | network | unusual_outbound | line 89 | Connection to rare destination IP with no other indicators

6. After all categories have been searched, read your findings file using file_read. Review all findings together.

7. Report your findings:

   If you have INCIDENT INDICATOR findings that are correlated across at least 2 categories and form a coherent timeline of activity, create a highly structured, sequential Event Stream that simulates the flow of time and emphasizes the progression of the incident. Each event in the timeline should show: timestamp (if available), category, what happened, and which log line it came from.

   If you have SUSPICIOUS ACTIVITY findings but no incident indicators, list each suspicious finding with its category, description, and why you flagged it. Recommend whether the analyst should investigate further.

   If you have no findings at all, inform the user that no malicious or suspicious activity was found in the queried log data.
