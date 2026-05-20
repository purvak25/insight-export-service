# INSIGHT-2147

## Summary
Lambda costs increased suddenly after export optimization deployment.

## Severity
P1 - Critical

## Symptoms
- Scheduled exports delayed
- Lambda timeout spikes
- Repeated API requests
- Increased AWS spend
- Duplicate report records

## Root Cause
Pagination token not updated inside export loop.

## Resolution
- Added token update logic
- Added duplicate token detection
- Added max iteration safeguard

## Status
Resolved
