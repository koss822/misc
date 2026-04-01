# claude-log-analyzer

> Reduced MTTR from ~40 min to ~8 min by surfacing root causes from wall-of-text log dumps instantly.

Streams application or system logs to the Claude API for anomaly detection, error correlation,
and incident summarization. Handles large logs by chunking and optionally synthesizing a
single final report across all chunks.

## Usage

```bash
# Analyze a log file
python analyze.py --log /var/log/app.log

# Read from stdin (pipe from kubectl)
kubectl logs -n prod deploy/api --since=1h | python analyze.py --stdin

# Custom output path
python analyze.py --log app.log --output incidents/2025-04-01.md

# Dry-run (no API calls)
python analyze.py --log app.log --dry-run
```

## Output

Writes `analysis.md` with sections:
- **Errors** — detected exceptions with line references
- **Patterns** — repeated failures, correlations
- **Timeline** — chronological event sequence
- **Hypothesis** — likely root cause
- **Actions** — immediate remediation steps

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```
