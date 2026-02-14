.PHONY: help run-ingestion run-stream run-cqrs run-saga run-agent

help:
	@echo "Available commands:"
	@echo "  make run-ingestion   - Run Ingestion Layer (Go)"
	@echo "  make run-stream      - Run Stream Processor (Go)"
	@echo "  make run-cqrs        - Run CQRS Updater (Go)"
	@echo "  make run-saga        - Run Saga Pattern (Go)"
	@echo "  make run-agent       - Run AI Agent Interactor (Python)"

run-ingestion:
	@echo "Running Ingestion Layer Mock..."
	go run ingestion_layer.go

run-stream:
	@echo "Running Stream Processor Mock..."
	go run stream_processor.go

run-cqrs:
	@echo "Running CQRS/Read-Aside Mock..."
	go run cqrs_updater.go

run-saga:
	@echo "Running Saga Pattern Mock..."
	go run saga_pattern.go

run-agent:
	@echo "Running AI Agent Interactor..."
	python3 agent_interactor.py
