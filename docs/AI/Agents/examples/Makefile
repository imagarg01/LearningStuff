.PHONY: setup run-single run-reflection run-multi run-prod-funnel run-stateful-persona run-companion-primitives

PYTHON ?= python3

setup:
	pip install -r requirements.txt

run-single:
	$(PYTHON) 01_single_agent.py

run-reflection:
	$(PYTHON) 02_reflection_agent.py

run-multi:
	$(PYTHON) 03_multi_agent_orchestrator.py

run-prod-funnel:
	$(PYTHON) 04_production_ready_agent_funnel.py

run-stateful-persona:
	$(PYTHON) 05_stateful_decision_recovery_and_persona.py

run-companion-primitives:
	$(PYTHON) 06_companion_primitives_suite.py
