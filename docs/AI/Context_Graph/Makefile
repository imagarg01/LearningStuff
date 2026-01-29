# Makefile for Context Graph Examples
# =================================

# Python executable to use
PYTHON := python3

# Virtual environment directory
VENV := venv

# Default target: show help
.PHONY: help
help:
	@echo "Context Graph Examples - Makefile"
	@echo "================================="
	@echo "Available commands:"
	@echo "  make setup        : Create virtual environment and install dependencies"
	@echo "  make clean        : Remove virtual environment and cached files"
	@echo "  make build-graph  : Run simple_graph_builder.py to extract and load graph data"
	@echo "  make retrieve     : Run advanced_retrieval.py to demo GraphRAG"
	@echo ""
	@echo "Note: Ensure you have a .env file with OPENAI_API_KEY and NEO4J credentials set."

# Create virtual environment and install dependencies
.PHONY: setup
setup:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing requirements..."
	./$(VENV)/bin/pip install -r requirements.txt
	@echo "Setup complete. To activate venv: source $(VENV)/bin/activate"

# Run the Graph Builder Example
.PHONY: build-graph
build-graph:
	@echo "Running Graph Builder Example..."
	@# Check if venv exists, otherwise use system python (or fail)
	@if [ -d "$(VENV)" ]; then \
		./$(VENV)/bin/python simple_graph_builder.py; \
	else \
		$(PYTHON) simple_graph_builder.py; \
	fi

# Run the Retrieval Example
.PHONY: retrieve
retrieve:
	@echo "Running Advanced Retrieval (GraphRAG) Example..."
	@if [ -d "$(VENV)" ]; then \
		./$(VENV)/bin/python advanced_retrieval.py; \
	else \
		$(PYTHON) advanced_retrieval.py; \
	fi

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Clean complete."
