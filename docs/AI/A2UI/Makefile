# A2UI Examples Makefile
# Run Python examples and full-stack demos

.PHONY: all help install basic data-binding events streaming restaurant clean server demo

# Default target
all: help

help:
	@echo "A2UI Examples"
	@echo "============="
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "🐍 Python-Only Examples:"
	@echo "  basic        - Run basic agent (profile card JSONL)"
	@echo "  data-binding - Run data binding demonstration"
	@echo "  events       - Run event handling examples"
	@echo "  streaming    - Run streaming UI patterns"
	@echo "  restaurant   - Run restaurant finder (Python only)"
	@echo "  all-examples - Run all Python examples"
	@echo ""
	@echo "🌐 Full-Stack Demos (Python + Browser):"
	@echo "  server       - Start the A2UI demo server"
	@echo "  demo         - Start server and open in browser"
	@echo ""
	@echo "🛠️  Utilities:"
	@echo "  install      - Install Python dependencies"
	@echo "  validate     - Validate all Python files"
	@echo "  clean        - Clean generated files"
	@echo ""

# =============================================================================
# Setup
# =============================================================================

install:
	@echo "📦 Installing dependencies..."
	pip install -r src/requirements.txt
	@echo "✅ Done!"

validate:
	@echo "🔍 Validating Python files..."
	python -m py_compile src/01_basic_agent.py
	python -m py_compile src/02_data_binding.py
	python -m py_compile src/03_event_handling.py
	python -m py_compile src/04_streaming_ui.py
	python -m py_compile src/05_restaurant_finder.py
	python -m py_compile server.py
	@echo "✅ All files valid!"

# =============================================================================
# Python-Only Examples
# =============================================================================

basic:
	@echo ""
	@echo "🚀 Running Basic Agent Example..."
	@echo ""
	python src/01_basic_agent.py

data-binding:
	@echo ""
	@echo "🔗 Running Data Binding Example..."
	@echo ""
	python src/02_data_binding.py

events:
	@echo ""
	@echo "🖱️  Running Event Handling Examples..."
	@echo ""
	python src/03_event_handling.py

streaming:
	@echo ""
	@echo "📡 Running Streaming UI Example..."
	@echo ""
	python src/04_streaming_ui.py

restaurant:
	@echo ""
	@echo "🍽️  Running Restaurant Finder (Python)..."
	@echo ""
	python src/05_restaurant_finder.py

all-examples: basic data-binding events streaming restaurant
	@echo ""
	@echo "✅ All Python examples completed!"

# =============================================================================
# Full-Stack Demos
# =============================================================================

server:
	@echo ""
	@echo "🌐 Starting A2UI Demo Server..."
	@echo "📍 Visit: http://localhost:8000"
	@echo ""
	@echo "Available demos:"
	@echo "  - http://localhost:8000/profile    (Profile Card)"
	@echo "  - http://localhost:8000/counter    (Interactive Counter)"
	@echo "  - http://localhost:8000/restaurant (Restaurant Finder)"
	@echo ""
	@echo "Press Ctrl+C to stop the server"
	@echo ""
	python server.py

demo: 
	@echo ""
	@echo "🚀 Starting A2UI Demo..."
	@echo ""
	@# Start server in background and open browser
	@(sleep 2 && open http://localhost:8000) &
	python server.py

# =============================================================================
# Cleanup
# =============================================================================

clean:
	@echo "🧹 Cleaning..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean complete!"
