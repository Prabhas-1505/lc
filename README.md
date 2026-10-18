# Daily LeetCode Practice

This GitHub Actions workflow generates a **daily set of 3 LeetCode problems** (1 Easy, 1 Medium, 1 Hard) at approximately 8:00 PM India Standard Time.

## What it does
- Selects problems deterministically, cycling through the catalogue without repeating within each difficulty until its pool runs out.
- Produces a dated Markdown task sheet with direct LeetCode links and C++ reference solutions.
- Compile-checks all catalogue C++ solutions for syntax before generating the sheet.
- Adds the task sheet to the GitHub Actions job summary and uploads it as an artifact.
- Supports manual runs using **Actions → Daily LeetCode Practice → Run workflow**.

## What it does not do
- Reference solutions are included, but they have only syntax checks, not LeetCode judge validation.
- It does **not** log into LeetCode, run official LeetCode tests, submit solutions, or verify Accepted status.
- An authenticated LeetCode submission integration would need to be designed and verified separately. Do not commit passwords, session cookies, CSRF tokens or any credentials here.

## Schedule
GitHub Actions cron is `30 14 * * *` (14:30 UTC = 20:00 IST); scheduled executions may be delayed by GitHub.

## Files
- `problems.json`: catalogue of selectable problems.
- `solutions.json`: C++ reference solutions for all catalogue problems.
- `scripts/check_solutions.py`: C++ syntax checks.
- `scripts/daily.py`: selection and task-sheet generator.
- `.github/workflows/daily.yml`: scheduled CI workflow.

**Security:** This repository was public at setup. Use private repository visibility before adding any confidential data. Credentials belong in GitHub Actions Secrets, never source files.

## Intended LeetCode account
- Profile: https://leetcode.com/u/prabhasavvaru_1/
- Username: `prabhasavvaru_1`
- This is a target profile reference only, **not** a connected or authenticated LeetCode session.

## Prioritizing questions you have not solved
The daily selection now excludes:
1. Problem slugs listed in `solved.json` (maintained by you).
2. Any problems returned by LeetCode's public **recent Accepted submissions** query (when available).

**Limitation:** Recent Accepted submissions are not your full solved history. A problem may still be suggested even if you solved it long ago. If LeetCode blocks the public query, the workflow continues with local exclusions and warns in the output. For fully accurate unsolved filtering, a complete solved-problem export/sync is needed. Do not add session cookies to public source files.

This workflow prepares C++ reference solutions but **does not submit to LeetCode or change your solved count**.

## Submission integration research and safety gate (2026-10-18)

The third-party `@stevenli-phoenix/leetcode-cli` package documents `list --status unsolved`, `test`, and `submit` commands. It is **not an official LeetCode API** and requires session cookies. Reference: https://www.npmjs.com/package/@stevenli-phoenix/leetcode-cli

LeetCode's terms restrict processes operating while a user is not logged into the platform and prohibit crawling/scraping: https://leetcode.com/terms/. A scheduled remote bot using account cookies could violate those restrictions. **The repository intentionally does not store credentials, call unofficial submission endpoints, or perform unattended submissions.** Do not add LeetCode session cookies or CSRF tokens to this public repository.

### Ready for verification
The daily workflow now exports individual `.cpp` reference files along with the Markdown sheet. Download the `leetcode-practice` artifact and review code before submitting through the LeetCode editor. The solution generator and syntax checker are functional, but they do **not** prove Accepted results.

If LeetCode explicitly authorizes an automated submission integration, confirm its approved method and permissions before implementing any authenticated execution.
