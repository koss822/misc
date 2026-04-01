#!/usr/bin/env python3
"""
langchain-runbook-qa — Conversational Q&A over Markdown runbooks using FAISS + Claude.

Usage:
    # Index runbooks and ask a question:
    python qa.py --docs ./runbooks "How do I roll back a Helm release?"

    # Reindex (rebuild vector store):
    python qa.py --docs ./runbooks --reindex "What is the on-call escalation path?"

    # Dry-run (no API calls):
    python qa.py --docs ./runbooks --dry-run "Any question"
"""

import argparse
import sys
from pathlib import Path

FAISS_INDEX_DIR = ".faiss_index"


def load_documents(docs_dir: Path) -> list[dict]:
    docs = []
    for path in sorted(docs_dir.rglob("*.md")):
        text = path.read_text(errors="replace")
        docs.append({"source": str(path), "text": text})
    for path in sorted(docs_dir.rglob("*.txt")):
        text = path.read_text(errors="replace")
        docs.append({"source": str(path), "text": text})
    return docs


def chunk_documents(docs: list[dict], chunk_size: int = 1000, overlap: int = 200) -> list[dict]:
    chunks = []
    for doc in docs:
        text = doc["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append({"source": doc["source"], "text": chunk_text, "start": start})
            start += chunk_size - overlap
    return chunks


def build_index(chunks: list[dict]):
    from langchain_anthropic import ChatAnthropic
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings

    print(f"[*] Embedding {len(chunks)} chunks...", file=sys.stderr)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
    store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    store.save_local(FAISS_INDEX_DIR)
    print(f"[+] Index saved to {FAISS_INDEX_DIR}/", file=sys.stderr)
    return store


def load_index():
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(FAISS_INDEX_DIR, embeddings, allow_dangerous_deserialization=True)


def answer_question(store, question: str) -> str:
    from langchain_anthropic import ChatAnthropic
    from langchain.chains import RetrievalQA

    llm = ChatAnthropic(model="claude-sonnet-4-6", max_tokens=1024)
    retriever = store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )
    result = chain.invoke({"query": question})
    answer = result["result"]
    sources = sorted({doc.metadata["source"] for doc in result["source_documents"]})
    if sources:
        answer += "\n\n**Sources:**\n" + "\n".join(f"- `{s}`" for s in sources)
    return answer


def dry_run_answer(question: str, chunks: list[dict]) -> str:
    relevant = [c for c in chunks if any(w in c["text"].lower() for w in question.lower().split())][:3]
    sources = sorted({c["source"] for c in relevant}) or ["(no matching docs)"]
    return (
        f"[dry-run] Question: **{question}**\n\n"
        f"Would search {len(chunks)} chunks across {len(set(c['source'] for c in chunks))} file(s).\n\n"
        f"Closest sources:\n" + "\n".join(f"- `{s}`" for s in sources)
    )


def main():
    parser = argparse.ArgumentParser(description="Q&A over runbooks using FAISS + Claude")
    parser.add_argument("question", help="Question to answer")
    parser.add_argument("--docs", required=True, metavar="DIR", help="Directory containing Markdown runbooks")
    parser.add_argument("--reindex", action="store_true", help="Rebuild the FAISS index from scratch")
    parser.add_argument("--dry-run", action="store_true", help="Skip embedding and API calls")
    args = parser.parse_args()

    docs_dir = Path(args.docs)
    if not docs_dir.is_dir():
        print(f"Error: directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    docs = load_documents(docs_dir)
    if not docs:
        print(f"Error: no .md or .txt files found in {docs_dir}", file=sys.stderr)
        sys.exit(1)

    chunks = chunk_documents(docs)
    print(f"[*] Loaded {len(docs)} document(s), {len(chunks)} chunk(s)", file=sys.stderr)

    if args.dry_run:
        print(dry_run_answer(args.question, chunks))
        return

    index_path = Path(FAISS_INDEX_DIR)
    if args.reindex or not index_path.exists():
        store = build_index(chunks)
    else:
        print(f"[*] Loading existing index from {FAISS_INDEX_DIR}/", file=sys.stderr)
        store = load_index()

    print("[*] Querying...\n", file=sys.stderr)
    answer = answer_question(store, args.question)
    print(answer)


if __name__ == "__main__":
    main()
