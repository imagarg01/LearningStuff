# Makefile for Pydantic AI Examples

.PHONY: help install basic rag all clean

# Default python interpreter (assuming python3)
PYTHON := python3

help:
	@echo "Pydantic AI Examples"
	@echo "===================="
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install    - Install dependencies (pydantic)"
	@echo "  basic      - Run the Basic Structure example"
	@echo "  rag        - Run the RAG Extractor example"
	@echo "  all        - Run all examples"
	@echo "  clean      - Remove cache files"

install:
	$(PYTHON) -m pip install pydantic

basic:
	@echo ""
	@echo "🧪 Running Basic Structure Example..."
	@echo "-----------------------------------"
	$(PYTHON) src/basic_structure.py

rag:
	@echo ""
	@echo "📄 Running RAG Extractor Example..."
	@echo "---------------------------------"
	$(PYTHON) src/rag_extractor.py

all: basic rag
	@echo ""
	@echo "✅ All examples completed successfully."

clean:
	rm -rf src/__pycache__
