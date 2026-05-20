````md
# insight-export-service

Production incident simulation repository.

This project simulates a realistic backend production incident where a pagination optimization introduced an infinite loop in export processing, causing AWS Lambda timeouts, duplicate report generation, and increased infrastructure costs.

---

# Architecture

+----------------------+     +--------------------------+     +----------------------+
|  Reporting API       |---->|  insight-export-service  |---->|  Export Storage      |
|  (api.reporting.io)  |     |    (AWS Lambda/Python)   |     |  (S3 / Analytics)    |
+----------------------+     +--------------------------+     +----------------------+

---

# Components

src/pagination_client.py - Handles paginated export retrieval  
config/env.example - Environment configuration template  
docs/RCA.md - Root cause analysis documentation  
docs/aws-log-snippet.txt - CloudWatch production logs  
docs/slack-thread.md - Incident investigation discussion  
docs/jira-ticket.md - Jira incident summary  
docs/incident-timeline.md - Full production timeline  

---

# Export Flow

1. Scheduled export job triggered
2. Service requests paginated export data
3. Export batches processed sequentially
4. Records stored in downstream analytics systems
5. Metrics and logs emitted to CloudWatch

---

# Configuration Management

Environment variables (see config/env.example):

| Variable | Description | Default |
|----------|-------------|---------|
| EXPORT_API_URL | External reporting API | required |
| AWS_REGION | AWS deployment region | us-east-1 |
| LAMBDA_TIMEOUT | Lambda execution timeout | 900 |
| PAGE_SIZE | Export page size | 1000 |
| LOG_LEVEL | Logging verbosity | INFO |

---

# Incident Simulation

This repository contains the evolution of a realistic production outage.

---

# Stage 1 - Correct Implementation

Commit: Implement paginated export workflow

Pagination handled correctly with token progression.

Example:

```python
while next_token:
    response = fetch_page(next_token)
    next_token = response.get("next_token")
````

Exports completed successfully under production load.

---

# Stage 2 - Optimization Bug Introduced

Commit: Optimize export pagination processing

Developer refactored pagination loop during export optimization work.

Broken implementation:

```python
while next_token:
    response = fetch_page(next_token)
```

`next_token` was never updated after each API response.

This caused:

* repeated export requests
* infinite pagination loop
* Lambda timeout failures
* duplicate export processing
* AWS cost spikes

---

# Why it passed local testing

Local testing used mocked responses with small datasets.

The downstream API returned valid payloads, so the loop continued executing without immediate failures.

No long-running pagination scenarios were tested locally.

---

# Why it bypassed detection

* No automated tests validated pagination progression
* CI/CD pipeline lacked loop safeguard checks
* Code review focused primarily on performance optimization
* No duplicate-token detection existed
* Monitoring focused on failure rate instead of execution duration anomalies

---

# Stage 3 - Hotfix & Prevention

Commit: Fix pagination loop and add execution safeguards

Fixes added:

* pagination token update
* duplicate-token detection
* max iteration safeguards
* execution duration monitoring

---

# Debugging Walkthrough

If you were on-call during this incident:

1. Review CloudWatch alarms
2. Check Lambda duration metrics
3. Inspect repeated pagination tokens in logs
4. Identify missing token update in pagination loop
5. Deploy hotfix with safeguards
6. Monitor Lambda recovery metrics

See docs/aws-log-snippet.txt for realistic CloudWatch logs.

---

# Monitoring Metrics

During the incident, these metrics degraded significantly:

| Metric                   | Normal   | Incident |
| ------------------------ | -------- | -------- |
| export_duration          | ~8s      | 900s     |
| export_success_rate      | 98%      | 41%      |
| lambda_memory_usage      | 45%      | 92%      |
| duplicate_export_records | 0        | ~18,000  |
| lambda_concurrency       | baseline | 4x spike |

---

# Lessons Learned

* Pagination workflows require progression validation.
* Loop safeguards are critical in distributed systems.
* Duration anomalies should alert before timeout thresholds.
* Small optimization changes can create large-scale production failures.
* Observability significantly reduces incident resolution time.

---

# Repository Structure

insight-export-service/
├── src/
│   └── pagination_client.py
├── docs/
│   ├── jira-ticket.md
│   ├── slack-thread.md
│   ├── incident-timeline.md
│   ├── RCA.md
│   └── aws-log-snippet.txt
├── config/
│   └── env.example
├── README.md
└── .gitignore

---

# Git History

* 7f9a2d1 Fix pagination loop and add execution safeguards
* 5b2c8e4 Optimize export pagination processing
* 2d1a7f0 Implement paginated export workflow

---

# License

MIT - For educational and portfolio use only.

```
```
