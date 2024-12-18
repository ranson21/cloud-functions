# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON_FUNCTIONS_DIR = functions/python
NODE_FUNCTIONS_DIR = functions/nodejs
FUNCTIONS_FRAMEWORK_PORT ?= 8080
PYTHON = python3
VENV_DIR = .venv

# Help target
help:
	@echo "Available targets:"
	@echo "  install-deps     Install all dependencies for Python and Node.js functions"
	@echo "  install-python   Install Python dependencies in virtual environment"
	@echo "  install-node     Install Node.js dependencies"
	@echo "  run-python      Run Python function locally (specify FUNCTION=function_name)"
	@echo "  run-node        Run Node.js function locally (specify FUNCTION=function_name)"
	@echo "  test            Run all tests"
	@echo "  test-python     Run Python tests"
	@echo "  test-node       Run Node.js tests"
	@echo "  clean           Clean up temporary files and dependencies"
	@echo "  create-venv     Create Python virtual environment"

# Installation targets
install-deps: install-python install-node

create-venv:
	@echo "Creating Python virtual environment..."
	cd $(PYTHON_FUNCTIONS_DIR) && $(PYTHON) -m venv $(VENV_DIR)

install-python: create-venv
	@echo "Installing Python dependencies..."
	cd $(PYTHON_FUNCTIONS_DIR) && \
	. $(VENV_DIR)/bin/activate && \
	for dir in */; do \
		if [ -f "$$dir/requirements.txt" ]; then \
			pip install -r "$$dir/requirements.txt"; \
		fi \
	done && \
	deactivate

install-node:
	@echo "Installing Node.js dependencies..."
	cd $(NODE_FUNCTIONS_DIR) && npm install

# Run targets
run-python:
ifndef FUNCTION
	$(error FUNCTION name is required. Usage: make run-python FUNCTION=your_function_name)
endif
	@echo "Running Python function $(FUNCTION)..."
	cd $(PYTHON_FUNCTIONS_DIR)/$(FUNCTION) && \
	. ../$(VENV_DIR)/bin/activate && \
	functions-framework --target=$(FUNCTION) --source=main.py --port=$(FUNCTIONS_FRAMEWORK_PORT)

run-node:
ifndef FUNCTION
	$(error FUNCTION name is required. Usage: make run-node FUNCTION=your_function_name)
endif
	@echo "Running Node.js function $(FUNCTION)..."
	cd $(NODE_FUNCTIONS_DIR) && \
	npx functions-framework --target=$(FUNCTION) --port=$(FUNCTIONS_FRAMEWORK_PORT)

# Test targets
test: test-python test-node

test-python:
	@echo "Running Python tests..."
	cd $(PYTHON_FUNCTIONS_DIR) && \
	. $(VENV_DIR)/bin/activate && \
	python -m pytest && \
	deactivate

test-node:
	@echo "Running Node.js tests..."
	cd $(NODE_FUNCTIONS_DIR) && npm test

# Clean target
clean:
	@echo "Cleaning up..."
	rm -rf $(PYTHON_FUNCTIONS_DIR)/$(VENV_DIR)
	rm -rf $(PYTHON_FUNCTIONS_DIR)/__pycache__
	rm -rf $(PYTHON_FUNCTIONS_DIR)/.pytest_cache
	rm -rf $(NODE_FUNCTIONS_DIR)/node_modules
	find . -name "*.pyc" -delete