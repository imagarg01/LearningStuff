# =============================================================================
# AI Agent Skills: Engineering, Testing & Delivery Factory Suite
# =============================================================================

.PHONY: help efficiency dependency agnostic factory all validate clean

PYTHON ?= python3

.DEFAULT_GOAL := help

help:
	@echo "AI Agent Skills: Enterprise Engineering & Delivery Factory"
	@echo "=========================================================="
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python Examples:"
	@echo "  efficiency  - Q1: Static Token Budget Linter & Runtime OTel Efficiency (TAF & CAR)"
	@echo "  dependency  - Q2: Model Quality Dependency Benchmark & Cognitive Offloading"
	@echo "  agnostic    - Q3: Model-Agnostic Test Harness (Canonical AST + Sandbox + Pass^k)"
	@echo "  factory     - Q4: 6-Stage Skill Delivery Factory CI/CD Pipeline (SEP-2640 + SEP-414)"
	@echo "  all         - Run all 4 Skill Engineering demos"
	@echo ""
	@echo "🔧 Utilities:"
	@echo "  validate    - Validate all Python files"
	@echo "  clean       - Remove Python cache files"

efficiency:
	@echo ""
	@echo "🪙 Running Token Efficiency Linter & Runtime OTel Analyzer..."
	@echo ""
	$(PYTHON) src/01_token_efficiency_analyzer.py

dependency:
	@echo ""
	@echo "🧠 Running Model Quality Dependency & Cognitive Offloading Benchmark..."
	@echo ""
	$(PYTHON) src/02_model_dependency_benchmark.py

agnostic:
	@echo ""
	@echo "🧪 Running Model-Agnostic Skill Test Harness..."
	@echo ""
	$(PYTHON) src/03_model_agnostic_test_harness.py

factory:
	@echo ""
	@echo "🏭 Running 6-Stage Skill Delivery Factory CI/CD Pipeline..."
	@echo ""
	$(PYTHON) src/04_skill_delivery_factory.py

all: efficiency dependency agnostic factory
	@echo ""
	@echo "✅ All AI Agent Skill Engineering examples completed!"

validate:
	@echo "🔍 Validating Python files..."
	$(PYTHON) -m py_compile src/01_token_efficiency_analyzer.py
	$(PYTHON) -m py_compile src/02_model_dependency_benchmark.py
	$(PYTHON) -m py_compile src/03_model_agnostic_test_harness.py
	$(PYTHON) -m py_compile src/04_skill_delivery_factory.py
	@echo "✅ All files valid!"

clean:
	@echo "🧹 Cleaning cache files..."
	rm -rf src/__pycache__
	rm -rf __pycache__
	@echo "✅ Cleaned!"
