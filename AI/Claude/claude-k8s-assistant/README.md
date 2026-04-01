# claude-k8s-assistant

> Ask your cluster questions in plain English — no more memorizing kubectl flags at 3am.

Natural-language Kubernetes troubleshooting. The tool selects the relevant `kubectl`
diagnostic commands based on your question, collects their output, and feeds everything
to Claude for a contextual diagnosis and remediation plan.

## Usage

```bash
# General health check
python assistant.py "Check overall cluster health"

# Crashloop diagnosis
python assistant.py "Why are my pods crashlooping in namespace prod?" --namespace prod

# Resource pressure
python assistant.py "Which pods are consuming the most memory?"

# Dry-run (uses fixture kubectl output, no API call)
python assistant.py "Check node status" --dry-run
```

## How it works

1. Parses keywords from your question (crash, memory, cpu, pending, node, …)
2. Runs the relevant subset of: `kubectl get nodes/pods/events`, `kubectl top`
3. Sends all outputs + your question to Claude
4. Prints the diagnosis with suggested remediation commands

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
# kubectl must be configured and pointing at your cluster
kubectl cluster-info
```
