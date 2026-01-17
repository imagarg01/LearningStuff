# =============================================================================
# A2A (Agent-to-Agent) Protocol Examples
# =============================================================================

.PHONY: help card client server validate all-examples clean

# Default target
.DEFAULT_GOAL := help

help:
	@echo "A2A Examples"
	@echo "============"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python Examples:"
	@echo "  card       - Generate Agent Cards"
	@echo "  client     - Task client demo"
	@echo "  server     - Agent server demo"
	@echo "  all        - Run all examples"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  validate   - Validate all Python files"
	@echo "  clean      - Remove Python cache files"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  00_overview.md        - What is A2A?"
	@echo "  01_agent_cards.md     - Discovery and capabilities"
	@echo "  02_tasks.md           - Task lifecycle"
	@echo "  03_communication.md   - JSON-RPC, streaming"
	@echo "  04_security.md        - Auth and security"
	@echo "  05_pros_and_cons.md   - Analysis"

# =============================================================================
# Python Examples
# =============================================================================

card:
	@echo ""
	@echo "📇 Running Agent Card Generator..."
	@echo ""
	python src/01_agent_card.py

client:
	@echo ""
	@echo "📤 Running Task Client Demo..."
	@echo ""
	python src/02_task_client.py

server:
	@echo ""
	@echo "🖥️  Running Agent Server Demo..."
	@echo ""
	python src/03_agent_server.py

all: card client server
	@echo ""
	@echo "✅ All A2A examples completed!"

all-examples: all

# =============================================================================
# Utilities
# =============================================================================

validate:
	@echo "🔍 Validating Python files..."
	python -m py_compile src/01_agent_card.py
	python -m py_compile src/02_task_client.py
	python -m py_compile src/03_agent_server.py
	@echo "✅ All files valid!"

clean:
	@echo "🧹 Cleaning cache files..."
	rm -rf src/__pycache__
	rm -rf __pycache__
	@echo "✅ Cleaned!"
