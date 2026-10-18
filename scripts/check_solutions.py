#!/usr/bin/env python3
"""Compile-check LeetCode C++ reference solutions in isolation."""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
catalogue = json.loads((ROOT / "problems.json").read_text(encoding="utf-8"))
solutions = json.loads((ROOT / "solutions.json").read_text(encoding="utf-8"))
expected = {p["slug"] for p in catalogue}
if set(solutions) != expected:
    raise SystemExit(f"Solution catalogue mismatch: missing={expected-set(solutions)}, extra={set(solutions)-expected}")
header = """
#include <bits/stdc++.h>
using namespace std;
struct ListNode { int val; ListNode *next; ListNode(int x=0):val(x),next(nullptr){} };
struct TreeNode { int val; TreeNode *left; TreeNode *right; TreeNode(int x=0):val(x),left(nullptr),right(nullptr){} };
"""
for slug, solution in solutions.items():
    result = subprocess.run(
        ["g++", "-std=c++17", "-x", "c++", "-fsyntax-only", "-"],
        input=header + "\n" + solution + "\n",
        text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        print(f"FAILED: {slug}\n{result.stderr}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Syntax OK: {slug}")
print(f"Validated {len(solutions)} C++ reference solutions (syntax only, not LeetCode tests).")
