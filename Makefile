.PHONY: help generate review profile material vocab lint fix format check

help:
	@echo "Available commands:"
	@echo "  make generate       - Generate daily task"
	@echo "  make review DATE=YYYY-MM-DD TASK=1  - Review task (default: TASK=1)"
	@echo "  make profile        - Show your learning profile and weaknesses"
	@echo "  make material       - List suggested learning materials"
	@echo "  make material TOPIC=\"Topic Name\"  - Generate specific material"
	@echo "  make vocab-stats    - Show vocabulary statistics"
	@echo "  make vocab-add WORD=\"word\" MEANING=\"meaning\"  - Add new vocabulary"
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

profile:
	uv run lingokeun profile

material:
	@if [ -z "$(TOPIC)" ]; then \
		uv run lingokeun material --list; \
	else \
		uv run lingokeun material --topic "$(TOPIC)"; \
	fi

vocab-stats:
	uv run lingokeun vocab --stats

vocab-add:
	@if [ -z "$(WORD)" ]; then \
		echo "Error: WORD is required. Usage: make vocab-add WORD=\"prominently\" TYPE=\"adv\" MEANING=\"secara menonjol\""; \
		exit 1; \
	fi
	@if [ -n "$(TYPE)" ] && [ -n "$(MEANING)" ]; then \
		uv run lingokeun vocab --add "$(WORD)" --type "$(TYPE)" --meaning "$(MEANING)"; \
	elif [ -n "$(TYPE)" ]; then \
		uv run lingokeun vocab --add "$(WORD)" --type "$(TYPE)"; \
	elif [ -n "$(MEANING)" ]; then \
		uv run lingokeun vocab --add "$(WORD)" --meaning "$(MEANING)"; \
	else \
		uv run lingokeun vocab --add "$(WORD)"; \
	fi

lint:
	uv run ruff check .

fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

check: lint
	uv run ruff format . --check
