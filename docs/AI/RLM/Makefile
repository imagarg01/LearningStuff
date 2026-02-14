.PHONY: help run-complex run-simple run-battery run-custom

help:
	@echo "Available commands:"
	@echo "  make run-complex   - Run the complex recursion example (compare 3 phones)"
	@echo "  make run-simple    - Run a simple single-step query"
	@echo "  make run-battery   - Run a specific battery lookup"
	@echo "  make run-custom QUERY=\"Your query here\" - Run with a custom query"

run-complex:
	@echo "Running Complex Recursive Task..."
	python3 rlm_simulation.py "Compare battery life of top 3 Android phones released in 2024"

run-simple:
	@echo "Running Simple Task..."
	python3 rlm_simulation.py "Find top 3 Android phones of 2024"

run-battery:
	@echo "Running Specific Task..."
	python3 rlm_simulation.py "Get battery size for Samsung S24 Ultra"

run-custom:
	@echo "Running Custom Query: $(QUERY)"
	python3 rlm_simulation.py $(QUERY)
