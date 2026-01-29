# Makefile for RAG Strategies Examples

PYTHON := python3
PIP := pip

.PHONY: install naive hybrid rerank query_exp all help

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make naive        - Run Naive RAG example"
	@echo "  make hybrid       - Run Hybrid Search example"
	@echo "  make rerank       - Run Re-ranking example"
	@echo "  make query_exp    - Run Query Expansion example"
	@echo "  make all          - Run all examples"

install:
	$(PIP) install -r requirements.txt

naive:
	$(PYTHON) naive_rag.py

hybrid:
	$(PYTHON) hybrid_search.py

rerank:
	$(PYTHON) reranking.py

query_exp:
	$(PYTHON) query_expansion.py

eval:
	$(PYTHON) evaluate_rag.py

test-deepeval:
	pytest test_deepeval.py

agentic:
	$(PYTHON) agentic_rag.py

chunking:
	$(PYTHON) chunking_methods.py

# TruLens requires DB init, often fails in simple CI environments without setup
trulens:
	$(PYTHON) test_trulens.py

all: naive hybrid rerank query_exp agentic
