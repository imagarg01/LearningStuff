# =============================================================================
# UCP (Universal Commerce Protocol) Examples
# =============================================================================

.PHONY: help profile checkout mcp validate all-examples clean

# Default target
.DEFAULT_GOAL := help

help:
	@echo "UCP Examples"
	@echo "============"
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python Examples:"
	@echo "  profile    - Generate UCP business profile"
	@echo "  checkout   - Run complete checkout flow demo"
	@echo "  mcp        - Demonstrate MCP tool integration"
	@echo "  all        - Run all examples"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  validate   - Validate all Python files"
	@echo "  clean      - Remove Python cache files"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  00_overview.md        - Protocol overview"
	@echo "  01_core_concepts.md   - Profiles, Capabilities, Extensions"
	@echo "  02_capabilities.md    - Checkout, Identity, Order, Payment"
	@echo "  03_transport_layers.md - REST, MCP, A2A, Embedded"
	@echo "  04_payment_security.md - AP2, OAuth, PCI"
	@echo "  05_pros_and_cons.md   - Analysis and decision matrix"

# =============================================================================
# Python Examples
# =============================================================================

profile:
	@echo ""
	@echo "📦 Running Business Profile Generator..."
	@echo ""
	python src/01_business_profile.py

checkout:
	@echo ""
	@echo "🛒 Running Checkout Flow Demo..."
	@echo ""
	python src/02_checkout_flow.py

mcp:
	@echo ""
	@echo "🔧 Running MCP Integration Demo..."
	@echo ""
	python src/03_mcp_integration.py

all: profile checkout mcp
	@echo ""
	@echo "✅ All examples completed!"

# Alias for all
all-examples: all

# =============================================================================
# Utilities
# =============================================================================

validate:
	@echo "🔍 Validating Python files..."
	python -m py_compile src/01_business_profile.py
	python -m py_compile src/02_checkout_flow.py
	python -m py_compile src/03_mcp_integration.py
	@echo "✅ All files valid!"

clean:
	@echo "🧹 Cleaning cache files..."
	rm -rf src/__pycache__
	rm -rf __pycache__
	@echo "✅ Cleaned!"
