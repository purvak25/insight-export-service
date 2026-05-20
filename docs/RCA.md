# Root Cause Analysis: INSIGHT-2147

**Incident:** Lambda costs increased suddenly  
**Date:** 2024-05-18  
**Duration:** 55 minutes  
**Severity:** P1 - Critical  
**Status:** Resolved

---

## 1. Incident Summary

On May 18, 2024, the `insight-export-service` began repeatedly fetching the same export page due to a pagination loop bug introduced during optimization work.

This caused long-running Lambda executions, increased memory utilization, duplicate processing, and a sudden spike in AWS costs.

---

## 2. Root Cause

A pagination optimization introduced a loop where `next_token` was never updated after each API request.

Broken logic:

```python
while next_token:
    response = fetch_page(next_token)
