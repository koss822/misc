#!/usr/bin/env python3
"""
claude-log-analyzer — Feed logs to Claude for anomaly detection and incident summarization.

Usage:
    python analyze.py --log /var/log/app.log
    python analyze.py --log /var/log/app.log --dry-run
    cat /var/log/app.log | python analyze.py --stdin
"""

import argparse
import sys
import os
import re
from datetime import datetime
from pathlib import Path

import anthropic

CHUNK_SIZE = 8000  # characters per API call
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """You are an expert SRE analyzing application and system logs.
Your job is to detect anomalies, identify error patterns, and produce a concise incident summary.
Always respond in structured Markdown."""

ANALYSIS_PROMPT = """Analyze the following log chunk and identify:
1. Errors and exceptions (with line numbers if present)
2. Anomalous patterns or repeated failures
3. Timeline of significant events
4. Root cause hypothesis (if determinable)
5. Recommended immediate actions

Log chunk:
```
{log_chunk}
```

Respond in Markdown with sections: ## Errors, ## Patterns, ## Timeline, ## Hypothesis, ## Actions."""


def chunk_text(text: str, size: int) -> list[str]:
    lines = text.splitlines(keepends=True)
    chunks, current = [], []
    current_len = 0
    for line in lines:
        if current_len + len(line) > size and current:
            chunks.append("".join(current))
            current, current_len = [], 0
        current.append(line)
        current_len += len(line)
    if current:
        chunks.append("".join(current))
    return chunks


def analyze_logs(log_text: str, dry_run: bool = False) -> str:
    chunks = chunk_text(log_text, CHUNK_SIZE)
    print(f"[*] Log size: {len(log_text)} chars, {len(chunks)} chunk(s)", file=sys.stderr)

    if dry_run:
        print("[dry-run] Would send to Claude API. Returning fixture output.", file=sys.stderr)
        return f"""# Log Analysis (dry-run)

## Errors
- [dry-run] No real errors detected — this is fixture output.

## Patterns
- Log contains {len(log_text.splitlines())} lines split into {len(chunks)} chunk(s).

## Timeline
- Analysis would cover the full log timerange.

## Hypothesis
- dry-run mode: no actual analysis performed.

## Actions
- Set `ANTHROPIC_API_KEY` and run without `--dry-run`.
"""

    client = anthropic.Anthropic()
    analyses = []

    for i, chunk in enumerate(chunks, 1):
        print(f"[*] Analyzing chunk {i}/{len(chunks)}...", file=sys.stderr)
        message = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": ANALYSIS_PROMPT.format(log_chunk=chunk)}],
        )
        analyses.append(message.content[0].text)

    if len(analyses) == 1:
        return analyses[0]

    # Merge multi-chunk analyses with a final synthesis call
    print("[*] Synthesizing multi-chunk analysis...", file=sys.stderr)
    combined = "\n\n---\n\n".join(f"### Chunk {i+1}\n{a}" for i, a in enumerate(analyses))
    synthesis = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Synthesize these per-chunk analyses into one final incident report:\n\n{combined}",
        }],
    )
    return synthesis.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Analyze logs with Claude AI")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--log", metavar="FILE", help="Path to log file")
    source.add_argument("--stdin", action="store_true", help="Read log from stdin")
    parser.add_argument("--output", metavar="FILE", default="analysis.md", help="Output file (default: analysis.md)")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, use fixture output")
    args = parser.parse_args()

    if args.stdin:
        log_text = sys.stdin.read()
    else:
        log_path = Path(args.log)
        if not log_path.exists():
            print(f"Error: file not found: {log_path}", file=sys.stderr)
            sys.exit(1)
        log_text = log_path.read_text(errors="replace")

    if not log_text.strip():
        print("Error: log input is empty", file=sys.stderr)
        sys.exit(1)

    result = analyze_logs(log_text, dry_run=args.dry_run)

    header = f"# Incident Log Analysis\n\n**Generated:** {datetime.utcnow().isoformat()}Z  \n**Model:** {MODEL}\n\n---\n\n"
    output = Path(args.output)
    output.write_text(header + result)
    print(f"[+] Analysis written to {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
