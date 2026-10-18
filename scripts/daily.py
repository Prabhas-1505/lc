#!/usr/bin/env python3
"""Prepare 3 C++ practice solutions, excluding known solved questions.

Public LeetCode recent submissions are incomplete; candidates are NOT guaranteed unsolved.
"""
import datetime as dt
import json
import os
import pathlib
import random
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
USER = "prabhasavvaru_1"
catalogue = json.loads((ROOT / "problems.json").read_text(encoding="utf-8"))
solutions = json.loads((ROOT / "solutions.json").read_text(encoding="utf-8"))
known_solved = set(json.loads((ROOT / "solved.json").read_text(encoding="utf-8")))
if not all(isinstance(slug, str) for slug in known_solved):
    raise SystemExit("solved.json must be an array of problem slugs.")

# Recent public Accepted submissions: only a partial history, not the full solved list.
query = """query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    titleSlug
  }
}"""
fetch_status = "Public recent Accepted submissions unavailable"
try:
    body = json.dumps({"query": query, "variables": {"username": USER, "limit": 20}}).encode()
    request = urllib.request.Request(
        "https://leetcode.com/graphql/",
        data=body,
        headers={"Content-Type": "application/json", "Referer": "https://leetcode.com/",
                 "User-Agent": "Mozilla/5.0 (compatible; daily-practice/1.0)"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=12) as response:
        response_data = json.load(response)
    rows = response_data.get("data", {}).get("recentAcSubmissionList")
    if not isinstance(rows, list):
        raise ValueError("GraphQL response missing recent accepted submissions")
    known_solved.update(row["titleSlug"] for row in rows if isinstance(row, dict) and isinstance(row.get("titleSlug"), str))
    fetch_status = f"Checked {len(rows)} recent Accepted submissions (not complete history)"
except (OSError, ValueError, KeyError, TypeError) as error:
    print(f"WARNING: Could not check recent Accepted submissions: {error}")

today = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).date()
day = max(0, (today - dt.date(2026, 10, 19)).days)
selected = []
for level in ("Easy", "Medium", "Hard"):
    pool = [p for p in catalogue if p["difficulty"] == level and p["slug"] not in known_solved]
    if not pool:
        raise SystemExit(f"No available {level} problems after known-solved filtering. Expand problems.json.")
    # Daily deterministic cycle with only currently eligible problems.
    rng = random.Random(f"daily-lc:{level}:{today.isoformat()}")
    selected.append(rng.choice(pool))

output = [f"# LeetCode practice — {today.isoformat()}", "",
          f"Account: https://leetcode.com/u/{USER}/", "",
          "**Status: candidate unsolved questions, not verified against full account history.**",
          f"Filter: {fetch_status}; plus locally recorded solved.json entries.",
          "This workflow does not submit solutions or increase the LeetCode solved count.", ""]
for p in selected:
    output.append(f"- **{p['difficulty']}** — [{p['id']}. {p['title']}](https://leetcode.com/problems/{p['slug']}/)")
output += ["", "## C++ reference solutions", "",
           "These solutions are syntax-checked only, not accepted by LeetCode's judge.", ""]
for p in selected:
    code = solutions.get(p["slug"])
    if not code:
        raise SystemExit(f"Missing C++ solution for {p['slug']}")
    output.extend([f"### {p['title']}", "", "```cpp", code, "```", ""])
output += ["", "If any problem is already solved, add its slug to solved.json.", ""]
folder = ROOT / "output"
folder.mkdir(exist_ok=True)
dest = folder / f"{today.isoformat()}.md"
dest.write_text("\n".join(output), encoding="utf-8")
print(dest.read_text(encoding="utf-8"))
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write(dest.read_text(encoding="utf-8"))
