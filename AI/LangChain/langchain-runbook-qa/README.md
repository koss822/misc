# langchain-runbook-qa

> Your runbooks are already written — now make them instantly queryable.

Indexes a directory of Markdown runbooks into a local FAISS vector store and exposes
a conversational Q&A interface. Answers include source file references so you can
jump straight to the authoritative procedure.

## Usage

```bash
# First run — indexes docs and answers:
python qa.py --docs ./runbooks "How do I roll back a Helm release?"

# Subsequent runs reuse the index:
python qa.py --docs ./runbooks "What is the on-call escalation path?"

# Force reindex (e.g. after adding new runbooks):
python qa.py --docs ./runbooks --reindex "database failover steps"

# Dry-run:
python qa.py --docs ./runbooks --dry-run "any question"
```

## Example output

```
Answer: To roll back a Helm release, run:
  helm rollback <release-name> <revision>

You can list available revisions with `helm history <release-name>`.
If the rollback fails, check pod events with kubectl describe...

Sources:
- `helm-operations.md`
- `incident-response.md`
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

The FAISS index is saved to `.faiss_index/` on first run. Add it to `.gitignore`.
