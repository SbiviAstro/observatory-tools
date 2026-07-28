#!/usr/bin/env python3
"""
Bump the published version.

    python3 bump-version.py 7.15.000

Why this exists: the obvious way to bump a version is to search and replace the
old string with the new one across every file. That is wrong for changelog.html,
where old version numbers are *content* - the record of what shipped when. Doing
it that way once relabelled fifty historical entries with the current version and
destroyed the entire v7 history, which had to be reconstructed by hand.

So this script treats the changelog differently from everything else:

  * every page      - the version chip in the header is updated
  * changelog.html  - only the "- Current" marker moves; no other version
                      string in the file is touched

Run this BEFORE writing the new changelog entry. It works out what to replace by
reading which entry is currently marked "Current", so if the new entry is already
in place it will see the new version as current and refuse, having nothing to do.

Order:  1. bump-version.py <new>
        2. add the changelog entry, marked "- Current"
        3. build-csp-headers.py
"""
import re, sys
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", sys.argv[1]):
        sys.exit("usage: bump-version.py <major.minor.patch>   e.g. 7.15.000")
    new = sys.argv[1]

    chg = PUB / "changelog.html"
    if not chg.exists():
        sys.exit(f"changelog not found at {chg}")

    # find what is current now, so we know what we are replacing
    m = re.search(r'<div class="eyebrow">v([0-9.]+) &mdash; Current</div>', chg.read_text())
    if not m:
        m = re.search(r'<div class="eyebrow">v([0-9.]+) — Current</div>', chg.read_text())
    if not m:
        sys.exit("could not find the current entry in changelog.html")
    old = m.group(1)
    if old == new:
        sys.exit(f"v{new} is already current - nothing to do")

    touched = 0
    for f in sorted(PUB.glob("*.html")):
        c = f.read_text(encoding="utf-8")
        before = c
        if f.name == "changelog.html":
            # Only the Current marker moves. Historical entries are content and
            # must survive untouched.
            c = c.replace(f"v{old} — Current", f"v{old}")
            c = c.replace(f"v{old} &mdash; Current", f"v{old}")
        else:
            c = c.replace(f"v{old}", f"v{new}")
        if c != before:
            f.write_text(c, encoding="utf-8")
            touched += 1

    print(f"v{old} -> v{new}: {touched} file(s) updated")
    print("changelog history left intact; add the new entry manually, marked '— Current'")
    print("then run: python3 build-csp-headers.py")


if __name__ == "__main__":
    main()
