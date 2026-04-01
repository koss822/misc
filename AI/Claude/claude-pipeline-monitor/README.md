# claude-pipeline-monitor

> Diagnoses CI/CD pipeline failures in seconds instead of minutes of log-reading.

Reads a CI/CD pipeline failure log (GitHub Actions, GitLab CI, Jenkins) and uses the
Claude API to produce a structured JSON report with root cause, affected step, fix
suggestion, and severity. Exits with code 1 on HIGH/CRITICAL severity so it can be
wired into alerting workflows.

## Usage

```bash
# Analyze a pipeline log
python monitor.py --log pipeline.log

# Custom output path
python monitor.py --log pipeline.log --output reports/run-42.json

# Dry-run
python monitor.py --log pipeline.log --dry-run
```

## Output (`report.json`)

```json
{
  "root_cause": "pytest exited with code 1 — 3 test failures in test_api.py",
  "failed_step": "Run tests",
  "fix_suggestion": "Fix failing assertions in test_api.py lines 42, 87, 103",
  "severity": "HIGH",
  "error_lines": ["FAILED test_api.py::test_health - AssertionError"],
  "affected_files": ["test_api.py"],
  "_meta": { "analyzed_at": "...", "model": "claude-sonnet-4-6" }
}
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## CI/CD integration

```yaml
# GitHub Actions example
- name: Monitor pipeline on failure
  if: failure()
  run: python AI/Claude/claude-pipeline-monitor/monitor.py --log ${{ runner.temp }}/pipeline.log
```
