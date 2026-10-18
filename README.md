# Daily LeetCode Practice

This GitHub Actions workflow generates a **daily set of 3 LeetCode problems** (1 Easy, 1 Medium, 1 Hard) at approximately 8:00 PM India Standard Time.

## What it does
- Selects problems deterministically, cycling through the catalogue without repeating within each difficulty until its pool runs out.
- Produces a dated Markdown task sheet with direct LeetCode links.
- Adds the task sheet to the GitHub Actions job summary and uploads it as an artifact.
- Supports manual runs using **Actions → Daily LeetCode Practice → Run workflow**.

## What it does not do
- It does **not** log into LeetCode, solve problems, run against LeetCode tests, submit solutions, or verify Accepted status.
- An authenticated LeetCode submission integration would need to be designed and verified separately. Do not commit passwords, session cookies, CSRF tokens or any credentials here.

## Schedule
GitHub Actions cron is `30 14 * * *` (14:30 UTC = 20:00 IST); scheduled executions may be delayed by GitHub.

## Files
- `problems.json`: catalogue of selectable problems.
- `scripts/daily.py`: selection and task-sheet generator.
- `.github/workflows/daily.yml`: scheduled CI workflow.

**Security:** This repository was public at setup. Use private repository visibility before adding any confidential data. Credentials belong in GitHub Actions Secrets, never source files.

## Intended LeetCode account
- Profile: https://leetcode.com/u/prabhasavvaru_1/
- Username: `prabhasavvaru_1`
- This is a target profile reference only, **not** a connected or authenticated LeetCode session.
