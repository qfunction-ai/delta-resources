---
name: create-incident-timeline
description: This skill retrieves SumoLogic logs and analyzes them for high confidence security incidents, creating a timeline for each high confidence incident.
---

1. Prompt the user to provide the SumoLogic query to use and the time range over which to search

2. Use your query_sumologic tool to retrieve the SumoLogic logs according to the query and time range the user provided

3. Analyze the retrieved SumoLogic logs for security incidents that you are at least 90% confident that the logs correspond to an incident. 

4. For each high confidence security incident, create a timeline of the incidents in a readable format
