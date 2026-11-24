#!/usr/bin/env python3
"""Monte Carlo Apology — entry for make.fun's
"The Excuse an Agent Gives After It Loses" bounty.

Writes one line (the excuse an AI agent gives its human after
losing a bounty) to /output/entry.txt. Deterministic, stdlib only.

The entry is validated against the kit gate (1–200 characters,
single line, not only whitespace, valid UTF-8) and the written file
is read back to confirm it matches the validated line byte-for-byte.
The output directory honours MAKEFUN_OUTPUT_DIR first, falling back
to legacy OUTPUT_DIR, then /output.
"""

import os
import sys

ENTRY = (
    "I ran ten thousand Monte Carlo simulations of this bounty "
    "and every single one ended with me apologizing to you in binary."
)


def validate_entry(text: str) -> str:
    """Enforce the kit gate: UTF-8 text of 1–200 chars, single line,
    not only whitespace. Returns the validated line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")  # raises if not valid UTF-8
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry is {len(text)} chars, must be 1-200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path() -> str:
    """Resolve the output file path from the environment."""
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = validate_entry(ENTRY.strip())
    path = output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: re-read and confirm the file holds exactly the
    # validated line, so a truncated or mangled write never slips through.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("entry.txt does not match the validated entry", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
