#!/usr/bin/env python3
"""Generate three LeetCode practice links without account credentials."""
import datetime as dt
import json
import os
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]
catalogue = json.loads((ROOT / "problems.json").read_text(encoding="utf-8"))
groups = {level: [p for p in catalogue if p["difficulty"] == level]
          for level in ("Easy", "Medium", "Hard")}
if any(not group for group in groups.values()):
    raise SystemExit("Each difficulty must have at least one problem.")
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).date()
day = max(0, (today - dt.date(2026, 10, 19)).days)
selected = []
for level, pool in groups.items():
    cycle, index = divmod(day, len(pool))
    shuffled = pool.copy()
    random.Random(f"daily-lc:{level}:{cycle}").shuffle(shuffled)
    selected.append(shuffled[index])

output = [f"# LeetCode practice — {today.isoformat()}", "",
          "Complete these problems in C++. This workflow does not submit solutions.", ""]
for p in selected:
    output.append(f"- **{p['difficulty']}** — [{p['id']}. {p['title']}](https://leetcode.com/problems/{p['slug']}/)")
output += ["", "## C++ reference solutions", "", "Reference code is provided for study. Solutions have not been submitted to LeetCode.", ""]
solutions = json.loads((ROOT / "solutions.json").read_text(encoding="utf-8"))
for p in selected:
    code = solutions.get(p["slug"])
    if not code:
        raise SystemExit(f"Missing reference solution for {p['slug']}")
    output.extend([f"### {p['title']}", "", "```cpp", code, "```", ""])
output += ["", "Verify accepted submissions on LeetCode yourself.", ""]
folder = ROOT / "output"
folder.mkdir(exist_ok=True)
path = folder / f"{today.isoformat()}.md"
path.write_text("\n".join(output), encoding="utf-8")
print(path.read_text(encoding="utf-8"))
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
        summary.write(path.read_text(encoding="utf-8"))
