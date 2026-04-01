#!/usr/bin/env python3
"""
rag-docs-search — Semantic search over Markdown/text documentation with Claude-generated summaries.

Usage:
    # Index and search:
    python search.py --docs ./docs "How do I configure TLS?"

    # Reindex from scratch:
    python search.py --docs ./docs --reindex "deployment rollback procedure"

    # Just show raw chunks, no LLM summary:
    python search.py --docs ./docs --no-summary "oomkilled"

    # Dry-run:
    python search.py --docs ./docs --dry-run "any question"
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime

FAISS_INDEX_DIR = ".rag_index"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "claude-sonnet-4-6"
TOP_K = 5


def load_and_chunk(docs_dir: Path, chunk_size: int = 1000, overlap: int = 150) -> list[dict]:
    chunks = []
    extensions = ("*.md", "*.txt", "*.rst")
    for ext in extensions:
        for path in sorted(docs_dir.rglob(ext)):
            text = path.read_text(errors="replace")
            # Split on headings first for better context
            sections = split_by_headings(text)
            for section_title, section_text in sections:
                start = 0
                while start < len(section_text):
                    end = start + chunk_size
                    chunk = section_text[start:end].strip()
                    if chunk:
                        chunks.append({
                            "text": chunk,
                            "source": str(path.relative_to(docs_dir)),
                            "section": section_title,
                        })
                    start += chunk_size - overlap
    return chunks


def split_by_headings(text: str) -> list[tuple[str, str]]:
    import re
    parts = re.split(r"(?m)^(#{1,3} .+)$", text)
    if len(parts) <= 1:
        return [("", text)]
    sections = []
    current_title = ""
    current_body = []
    for part in parts:
        if part.startswith("#"):
            if current_body:
                sections.append((current_title, "".join(current_body)))
            current_title = part.strip("# ").strip()
            current_body = [part + "\n"]
        else:
            current_body.append(part)
    if current_body:
        sections.append((current_title, "".join(current_body)))
    return sections or [("", text)]


def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def build_index(chunks: list[dict]) -> object:
    from langchain_community.vectorstores import FAISS

    print(f"[*] Indexing {len(chunks)} chunks with {EMBED_MODEL}...", file=sys.stderr)
    embeddings = get_embeddings()
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "section": c["section"]} for c in chunks]
    store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    store.save_local(FAISS_INDEX_DIR)
    print(f"[+] Index saved to {FAISS_INDEX_DIR}/", file=sys.stderr)
    return store


def load_index() -> object:
    from langchain_community.vectorstores import FAISS
    return FAISS.load_local(FAISS_INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True)


def retrieve(store, query: str, k: int = TOP_K) -> list:
    return store.similarity_search_with_score(query, k=k)


def summarize_with_claude(query: str, chunks: list) -> str:
    import anthropic
    context = "\n\n---\n\n".join(
        f"[Source: {doc.metadata['source']}]\n{doc.page_content}"
        for doc, _ in chunks
    )
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=LLM_MODEL,
        max_tokens=1024,
        system="You are a technical documentation assistant. Answer questions accurately based only on the provided documentation excerpts. If the answer is not in the docs, say so.",
        messages=[{
            "role": "user",
            "content": f"Question: {query}\n\nDocumentation excerpts:\n{context}\n\nAnswer the question based on the excerpts above.",
        }],
    )
    return message.content[0].text


def print_results(query: str, chunks: list, summary: str | None) -> None:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}\n")

    if summary:
        print("## Answer\n")
        print(summary)
        print()

    print(f"## Top {len(chunks)} source chunk(s)\n")
    for i, (doc, score) in enumerate(chunks, 1):
        source = doc.metadata.get("source", "?")
        section = doc.metadata.get("section", "")
        heading = f"{source}" + (f" § {section}" if section else "")
        print(f"{i}. **{heading}** (score: {score:.3f})")
        print(f"   {doc.page_content[:200].replace(chr(10), ' ')}...")
        print()


def dry_run_output(query: str, chunks_count: int, files: list[str]) -> None:
    print(f"\n[dry-run] Query: {query}")
    print(f"[dry-run] Would search {chunks_count} indexed chunks across {len(files)} file(s):")
    for f in files[:5]:
        print(f"  - {f}")
    print("[dry-run] Skipping embedding and Claude API calls.\n")


def main():
    parser = argparse.ArgumentParser(description="Semantic search over docs with Claude summaries")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--docs", required=True, metavar="DIR", help="Documentation directory")
    parser.add_argument("--reindex", action="store_true", help="Rebuild index from scratch")
    parser.add_argument("--no-summary", action="store_true", help="Skip Claude summary, show raw chunks only")
    parser.add_argument("--top-k", type=int, default=TOP_K, metavar="N", help=f"Number of results (default: {TOP_K})")
    parser.add_argument("--dry-run", action="store_true", help="Skip all API calls")
    args = parser.parse_args()

    docs_dir = Path(args.docs)
    if not docs_dir.is_dir():
        print(f"Error: directory not found: {docs_dir}", file=sys.stderr)
        sys.exit(1)

    chunks = load_and_chunk(docs_dir)
    if not chunks:
        print(f"Error: no documents found in {docs_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Found {len(chunks)} chunk(s) from {len(set(c['source'] for c in chunks))} file(s)", file=sys.stderr)

    if args.dry_run:
        files = sorted(set(c["source"] for c in chunks))
        dry_run_output(args.query, len(chunks), files)
        return

    index_path = Path(FAISS_INDEX_DIR)
    if args.reindex or not index_path.exists():
        store = build_index(chunks)
    else:
        print(f"[*] Loading index from {FAISS_INDEX_DIR}/", file=sys.stderr)
        store = load_index()

    results = retrieve(store, args.query, k=args.top_k)

    summary = None
    if not args.no_summary and results:
        print("[*] Generating answer with Claude...", file=sys.stderr)
        summary = summarize_with_claude(args.query, results)

    print_results(args.query, results, summary)


if __name__ == "__main__":
    main()
