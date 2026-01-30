.PHONY: help generate review lint fix format check

help:
	@echo "Available commands:"
	@echo "  make generate       - Generate daily task"
	@echo "  make review DATE=YYYY-MM-DD TASK=1  - Review task (default: TASK=1)"
	@echo "  make lint           - Check code with ruff"
	@echo "  make fix            - Auto-fix linting issues"
	@echo "  make format         - Format code with ruff"
	@echo "  make check          - Run lint + format check"

generate:
	uv run lingokeun generate

review:
	@if [ -z "$(DATE)" ]; then \
		echo "Error: DATE is required. Usage: make review DATE=2026-01-29 TASK=1"; \
		exit 1; \
	fi
	uv run lingokeun review $(DATE) -t $(or $(TASK),1)

lint:
	uv run ruff check .

fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

check: lint
	uv run ruff format . --check
