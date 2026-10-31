# =============================================================================
# MCP (Model Context Protocol) Examples
# =============================================================================

.PHONY: help simple tools resources app skills validate all all-examples clean

PYTHON ?= python3

# Default target
.DEFAULT_GOAL := help

help:
	@echo "MCP Examples (2026-07-28 Specification)"
	@echo "======================================="
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python Examples:"
	@echo "  simple     - Stateless core, server/discover, Header Routing & Prompts"
	@echo "  tools      - outputSchema, structuredContent, SEP-1303 errors, MRTR & Tasks"
	@echo "  resources  - Static resources, RFC 6570 URI templates & resource_link"
	@echo "  app        - MCP Apps (ui:// scheme, visibility controls & theming)"
	@echo "  skills     - Skills Over MCP (SEP-2640), OAuth 2.1 RBAC & OpenTelemetry (SEP-414)"
	@echo "  all        - Run all examples"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  validate   - Validate all Python files"
	@echo "  clean      - Remove Python cache files"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  00_overview.md         - What is MCP?"
	@echo "  01_architecture.md     - Stateless Core, server/discover, MRTR & OTel"
	@echo "  02_primitives.md       - Tools, Resources, Prompts & Extensions"
	@echo "  03_transports.md       - Stateless HTTP, Header Routing & OAuth 2.1/OIDC"
	@echo "  04_building_servers.md - Implementation guide"
	@echo "  05_pros_and_cons.md    - Analysis & Spec Evolution"
	@echo "  06_mcp_app.md          - MCP Apps (ui:// Interactive UI Extension)"
	@echo "  src/README.md          - Guide to Python source examples & how to run"

# =============================================================================
# Python Examples
# =============================================================================

simple:
	@echo ""
	@echo "📡 Running Stateless Core, Header Routing & Prompts Demo..."
	@echo ""
	$(PYTHON) src/01_simple_server.py

tools:
	@echo ""
	@echo "🔧 Running Advanced Tools, MRTR & Tasks Demo..."
	@echo ""
	$(PYTHON) src/02_tool_server.py

resources:
	@echo ""
	@echo "📚 Running Resources & URI Templates Demo..."
	@echo ""
	$(PYTHON) src/03_resource_server.py

app:
	@echo ""
	@echo "🎨 Running MCP App (UI) Demo..."
	@echo ""
	$(PYTHON) src/04_mcp_app_server.py

skills:
	@echo ""
	@echo "🧠 Running Skills Over MCP (SEP-2640), Security & OpenTelemetry (SEP-414) Demo..."
	@echo ""
	$(PYTHON) src/05_skills_and_otel_server.py

all: simple tools resources app skills
	@echo ""
	@echo "✅ All MCP examples completed!"

all-examples: all

# =============================================================================
# Utilities
# =============================================================================

validate:
	@echo "🔍 Validating Python files..."
	$(PYTHON) -m py_compile src/01_simple_server.py
	$(PYTHON) -m py_compile src/02_tool_server.py
	$(PYTHON) -m py_compile src/03_resource_server.py
	$(PYTHON) -m py_compile src/04_mcp_app_server.py
	$(PYTHON) -m py_compile src/05_skills_and_otel_server.py
	@echo "✅ All files valid!"

clean:
	@echo "🧹 Cleaning cache files..."
	rm -rf src/__pycache__
	rm -rf __pycache__
	@echo "✅ Cleaned!"
