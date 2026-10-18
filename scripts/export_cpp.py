#!/usr/bin/env python3
"""Export today's prepared reference solutions as files for manual review.

No LeetCode authentication or submissions are performed.
"""
import datetime as dt
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
catalogue = json.loads((ROOT / "problems.json").read_text(encoding="utf-8"))
solutions = json.loads((ROOT / "solutions.json").read_text(encoding="utf-8"))
by_slug = {problem["slug"]: problem for problem in catalogue}
today = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).date()
sheet = ROOT / "output" / f"{today.isoformat()}.md"
if not sheet.exists():
    raise SystemExit(f"Missing practice sheet: {sheet}")

outdir = ROOT / "output" / "cpp"
outdir.mkdir(parents=True, exist_ok=True)
selected = [p for p in catalogue if f"https://leetcode.com/problems/{p['slug']}/" in sheet.read_text(encoding="utf-8")]
if len(selected) != 3:
    raise SystemExit(f"Expected 3 selected questions, got {len(selected)}")
for problem in selected:
    slug = problem["slug"]
    if slug not in solutions:
        raise SystemExit(f"Missing solution for {slug}")
    destination = outdir / f"{problem['id']}.{slug}.cpp"
    destination.write_text(
        f"// LeetCode {problem['id']} — {problem['title']}\n"
        "// Reference only; not tested against official judge.\n"
        "#include <bits/stdc++.h>\nusing namespace std;\n"
        "// LeetCode supplies ListNode and TreeNode definitions for linked-list/tree questions.\n"
        + solutions[slug] + "\n", encoding="utf-8")
    print(destination)
print("Generated files for manual review. No network submission occurred.")
