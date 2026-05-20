# Root Cause Analysis: INSIGHT-2147

**Incident:** Lambda costs increased suddenly
**Date:** 2024-05-18
**Duration:** 55 minutes (08:21 - 09:12 UTC)
**Severity:** P1 - Critical
**Status:** Resolved

---

# 1. Incident Summary

On May 18, 2024, the `insight-export-service` began repeatedly fetching the same export page due to a pagination loop introduced during export optimization work.

This resulted in long-running AWS Lambda executions, duplicate export processing, elevated memory utilization, and a significant increase in AWS infrastructure costs.

Approximately 18,000 duplicate export records were processed during the incident window before mitigation was completed.

---

# 2. Timeline

| Time (UTC) | Event                                                 |
| ---------- | ----------------------------------------------------- |
| 08:12      | Export optimization deployed to production            |
| 08:21      | CloudWatch alarm triggered (Lambda duration spike)    |
| 08:27      | Incident escalated to Platform and SRE teams          |
| 08:39      | Root cause identified (pagination token not updating) |
| 08:44      | Hotfix branch created                                 |
| 08:58      | Hotfix deployed to production                         |
| 09:03      | Lambda execution metrics normalized                   |
| 09:12      | Incident resolved                                     |

---

# 3. Root Cause

A pagination optimization introduced a loop in `src/pagination_client.py` where the `next_token` value was never updated after each API response.

Broken implementation:

```python
while next_token:
    response = fetch_page(next_token)
```

Expected implementation:

```python
while next_token:
    response = fetch_page(next_token)
    next_token = response.get("next_token")
```

This caused the service to continuously request the same export page instead of progressing through the paginated dataset.

### Why it passed local testing

Local testing used small datasets with mocked responses and did not simulate long-running paginated exports.

Because the downstream API returned valid responses, the loop continued processing without generating immediate application errors.

### Why it bypassed detection

* No automated tests validated pagination progression behavior
* CI/CD pipeline lacked loop safeguard validation
* Code review focused primarily on export performance optimization
* No duplicate-token detection existed in the export workflow
* Lambda execution alarms were configured only for failure rate, not duration anomalies

### Why it caused infrastructure impact

The repeated requests caused:

* continuous Lambda execution until timeout
* repeated processing of identical export records
* elevated memory utilization
* excessive downstream API traffic
* increased Lambda concurrency and AWS cost spikes

---

# 4. Technical Impact

* Lambda execution duration increased from ~8s to 900s
* Memory utilization exceeded 85% across export workers
* Approximately 18,000 duplicate export records processed
* Export scheduler backlog increased significantly
* AWS Cost Anomaly Detection triggered
* Export completion success rate dropped from 98% to 41%

### Error Types Observed

* `Task timed out after 900.00 seconds`
* `LambdaDurationHigh`
* duplicate pagination token warnings
* elevated concurrency threshold alerts

---

# 5. Business Impact

* Scheduled customer exports delayed
* Downstream analytics reports generated with duplicate data
* Internal reporting dashboards temporarily inconsistent
* Engineering and SRE teams diverted from sprint work for incident mitigation
* Increased AWS infrastructure spend during incident window
* Export SLAs breached for enterprise reporting clients

---

# 6. Resolution

* Added pagination token update logic
* Added duplicate-token validation
* Added max iteration safeguard
* Added execution duration monitoring
* Redeployed hotfix to production
* Reprocessed affected export batches after stabilization

Hotfix deployed to production within 19 minutes of root cause identification.

---

# 7. Preventive Actions

| Action                                       | Owner    | Ticket       | Target Date |
| -------------------------------------------- | -------- | ------------ | ----------- |
| Add pagination progression unit tests        | Backend  | INSIGHT-2148 | 2024-05-22  |
| Add duplicate-token detection                | Platform | INSIGHT-2149 | 2024-05-20  |
| Add Lambda duration anomaly alerts           | SRE      | INSIGHT-2150 | 2024-05-21  |
| Implement max pagination iteration safeguard | Backend  | INSIGHT-2151 | 2024-05-19  |
| Add export workflow integration tests        | QA       | INSIGHT-2152 | 2024-05-24  |
| Improve PR checklist for loop validation     | Platform | INSIGHT-2153 | 2024-05-20  |

---

# 8. Lessons Learned

* Pagination logic requires explicit progression validation.
* Long-running export workflows should always include iteration safeguards.
* Lambda duration anomalies should trigger alerts before timeout thresholds are reached.
* Small optimization changes can introduce severe production-scale failures.
* Duplicate-token detection should exist in all paginated processing systems.
* Performance-focused code reviews must also validate execution safety.

---

# 9. Attachments

* AWS Log Snippet
* Slack Thread
* Jira Ticket
* Incident Timeline
