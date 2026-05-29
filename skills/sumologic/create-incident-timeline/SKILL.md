---
name: create-incident-timeline
description: This skill retrieves SumoLogic logs and analyzes them for high confidence security incidents, creating a timeline for each high confidence incident.
---

1. Prompt the user to provide the SumoLogic query to use and the time range over which to search

2. Use your query_sumologic tool to retrieve the SumoLogic logs according to the query and time range the user provided

3. The query_sumologic tool returns a Python dictionary with a "file_path" key that tells you where the full results are stored. Use your grep_files tool to search the results file for indicators of compromise. Do NOT search for the literal string "LOLBINs" — instead, search for actual LOLBIN executable names and suspicious patterns. Run multiple grep_files calls for known LOLBINs such as: certutil, mshta, rundll32, regsvr32, msiexec, wscript, net user, Domain Admins, systeminfo, winrs, cscript, powershell with download cradles, cmd.exe with encoded commands, bitsadmin, certutil with -urlcache or -decode, mshta with http, and any base64-encoded command strings. Keep track of all findings.

4. If you have any findings from the previous step, determine whether they are correlated, and if they are, you have an incident.

5. If you have an incident, create a timeline of the incident from the flagged events. If you don't have an incident, inform the user of any flagged events and why you flagged them. If you don't have any flagged events at all, inform the user that no malicious activity was found
