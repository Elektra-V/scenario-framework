# Makefile for Recipe Agent Testing
# Provides convenient commands for common tasks

.PHONY: help setup install test test-verbose list-models run-scenario clean

help:
	@echo "Recipe Agent Testing - Available Commands"
	@echo ""
	@echo "  make setup      - Run automated setup script"
	@echo "  make install    - Install/update dependencies"
	@echo "  make test       - Run tests (quiet mode)"
	@echo "  make test-verbose - Run tests with verbose output"
	@echo "  make list-models - List available models from gateway"
	@echo "  make run-scenario - Run scenario standalone"
	@echo "  make clean      - Clean temporary files"
	@echo ""

setup:
	@echo "Running setup script..."
	@chmod +x setup.sh
	@./setup.sh

install:
	@echo "Installing/updating dependencies..."
	@uv sync

test:
	@echo "Running tests..."
	@uv run pytest -q

test-verbose:
	@echo "Running tests (verbose)..."
	@uv run pytest -v

list-models:
	@echo "Listing available models..."
	@uv run python list_models.py

run-scenario:
	@echo "Running scenario..."
	@uv run python run_scenario.py

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	@echo "✅ Clean complete"

