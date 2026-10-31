.PHONY: help run-simple run-judge meta-eval flywheel unified all validate clean

PYTHON ?= python3

.DEFAULT_GOAL := help

help:
	@echo "AI Evals: Meta-Evaluation, Continuous Flywheel & Unified Pipeline"
	@echo "================================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make run-simple  - Run the simple deterministic eval example"
	@echo "  make run-judge   - Run the LLM-as-a-judge eval example"
	@echo "  make meta-eval   - Measure Eval Quality (Mutation Score + Judge Calibration & Rogan-Gladen)"
	@echo "  make flywheel    - Continuous Eval Flywheel (OTel SEP-414 -> Golden Fixture + Pruning)"
	@echo "  make unified     - Unified Agent + Skill (SEP-2640) + MCP (2026-07-28) + 4-Layer Eval Pipeline"
	@echo "  make all         - Run all Eval examples"
	@echo "  make validate    - Byte-compile and validate all Python files"
	@echo "  make clean       - Remove Python cache files"

run-simple:
	$(PYTHON) src/simple_eval.py

run-judge:
	$(PYTHON) src/llm_judge_eval.py

meta-eval:
	$(PYTHON) src/03_meta_eval_quality_checker.py

flywheel:
	$(PYTHON) src/04_continuous_eval_flywheel.py

unified:
	$(PYTHON) src/05_unified_agent_mcp_skill_eval_pipeline.py

all: run-simple run-judge meta-eval flywheel unified

validate:
	$(PYTHON) -m py_compile src/simple_eval.py
	$(PYTHON) -m py_compile src/llm_judge_eval.py
	$(PYTHON) -m py_compile src/03_meta_eval_quality_checker.py
	$(PYTHON) -m py_compile src/04_continuous_eval_flywheel.py
	$(PYTHON) -m py_compile src/05_unified_agent_mcp_skill_eval_pipeline.py
	@echo "✅ All Eval Python scripts validated!"

clean:
	rm -rf src/__pycache__ __pycache__
