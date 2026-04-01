# rag-docs-search

> Turn any directory of Markdown files into a searchable, answerable knowledge base in one command.

Universal semantic search over Markdown, text, and RST documentation. Indexes your docs
into a local FAISS vector store using `all-MiniLM-L6-v2` embeddings (fully local, no API
for indexing), then answers queries with Claude using only the retrieved context.

## Usage

```bash
# Index and search (first run builds the index):
python search.py --docs ./docs "How do I configure TLS certificates?"

# Reindex after adding new docs:
python search.py --docs ./docs --reindex "deployment rollback"

# Skip Claude summary, show raw chunks only:
python search.py --docs ./docs --no-summary "oomkilled"

# Control number of results:
python search.py --docs ./docs --top-k 8 "prometheus scrape config"

# Dry-run:
python search.py --docs ./docs --dry-run "any question"
```

## Example output

```
Query: How do I configure TLS certificates?
============================================================

## Answer

To configure TLS certificates, create a Secret of type kubernetes.io/tls:
  kubectl create secret tls my-cert --cert=tls.crt --key=tls.key
Then reference it in your Ingress...

## Top 5 source chunk(s)

1. **ingress/tls.md § TLS Configuration** (score: 0.312)
   Create a TLS secret and reference it in the Ingress spec...

2. **cert-manager/quickstart.md § Issuing Certificates** (score: 0.387)
   ...
```

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

The FAISS index is saved to `.rag_index/`. Add it to `.gitignore`.
The embedding model (`all-MiniLM-L6-v2`) is downloaded on first run (~80 MB).
