# Slack Thread

**Channel:** #prod-export-incidents  
**Date:** 2024-05-18

---

**08:24 AM — SRE Engineer**

CloudWatch alarm triggered for `insight-export-prod`.

Seeing Lambda duration spikes across multiple export jobs.

---

**08:25 AM — Platform Engineer**

Concurrency also increased suddenly.

Current execution durations are close to timeout threshold.

---

**08:27 AM — Backend Engineer**

Checking latest deployment now.

Optimization patch was deployed around 08:12.

---

**08:30 AM — SRE Engineer**

Same pagination token keeps appearing in logs repeatedly.

Example:

INFO Fetching page token: eyJwYWdlIjoxfQ==
INFO Fetching page token: eyJwYWdlIjoxfQ==
INFO Fetching page token: eyJwYWdlIjoxfQ==

---

**08:32 AM — Backend Engineer**

Looks like `next_token` never updates after the API response.

That would explain:
- repeated requests
- memory increase
- Lambda timeout

---

**08:34 AM — Team Lead**

Can we temporarily disable scheduled exports?

Need to stop additional AWS cost increase.

---

**08:35 AM — Platform Engineer**

Scheduler paused for production exports.

Current running Lambdas still processing.

---

**08:39 AM — Backend Engineer**

Found the issue in pagination loop.

Current logic:

while next_token:
    response = fetch_page(next_token)

Missing:

next_token = response.get("next_token")

---

**08:42 AM — SRE Engineer**

AWS Cost Anomaly Detection also triggered.

Estimated spend already 4x higher than baseline.

---

**08:44 AM — Backend Engineer**

Creating hotfix branch now.

Adding:
- token update
- duplicate token validation
- max iteration safeguard

---

**08:58 AM — Platform Engineer**

Hotfix deployed to production.

Monitoring execution metrics now.

---

**09:03 AM — SRE Engineer**

Lambda durations returning to normal levels.

No repeated tokens observed anymore.

---

**09:07 AM — Team Lead**

Incident resolved.

Please prepare RCA and deployment notes before EOD.
