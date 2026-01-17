# =============================================================================
# MCP (Model Context Protocol) Examples
# =============================================================================

.PHONY: help simple tools resources validate all-examples clean

# Default target
.DEFAULT_GOAL := help

help:
	@echo "MCP Examples"
	@echo "============"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python Examples:"
	@echo "  simple     - Basic MCP server demo"
	@echo "  tools      - Multiple tools with JSON Schema"
	@echo "  resources  - Resource provider demo"
	@echo "  all        - Run all examples"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  validate   - Validate all Python files"
	@echo "  clean      - Remove Python cache files"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  00_overview.md        - What is MCP?"
	@echo "  01_architecture.md    - Host, Client, Server"
	@echo "  02_primitives.md      - Tools, Resources, Prompts"
	@echo "  03_transports.md      - Stdio, HTTP"
	@echo "  04_building_servers.md - Implementation guide"
	@echo "  05_pros_and_cons.md   - Analysis"

# =============================================================================
# Python Examples
# =============================================================================

simple:
	@echo ""
	@echo "📡 Running Simple MCP Server Demo..."
	@echo ""
	python src/01_simple_server.py

tools:
	@echo ""
	@echo "🔧 Running Tool Server Demo..."
	@echo ""
	python src/02_tool_server.py

resources:
	@echo ""
	@echo "📚 Running Resource Server Demo..."
	@echo ""
	python src/03_resource_server.py

all: simple tools resources
	@echo ""
	@echo "✅ All MCP examples completed!"

all-examples: all

# =============================================================================
# Utilities
# =============================================================================

validate:
	@echo "🔍 Validating Python files..."
	python -m py_compile src/01_simple_server.py
	python -m py_compile src/02_tool_server.py
	python -m py_compile src/03_resource_server.py
	@echo "✅ All files valid!"

clean:
	@echo "🧹 Cleaning cache files..."
	rm -rf src/__pycache__
	rm -rf __pycache__
	@echo "✅ Cleaned!"
