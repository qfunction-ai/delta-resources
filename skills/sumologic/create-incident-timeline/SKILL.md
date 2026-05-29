---
name: create-incident-timeline
description: This skill retrieves SumoLogic logs and analyzes them for high confidence security incidents, creating a timeline for each high confidence incident.
---

1. Prompt the user to provide the SumoLogic query to use and the time range over which to search

2. Use your query_sumologic tool to retrieve the SumoLogic logs according to the query and time range the user provided

3. The query_sumologic tool should return a list of strings. Go through each string in the list one by one and for each string, determine whether there are potentially malicious commands in the string. If there are, flag that string. Be sure to keep track of all strings in the list that were flagged

4. Now you have a list of flagged strings. Determine whether they are correlated, and if they are, you have an incident.

5. If you have an incident, create a timeline of the incident from the flagged strings. If you don't have an incident, inform the user of any flagged strings and why you flagged them. If you don't have any flagged strings at all, inform the user that no malicious activity was found 
