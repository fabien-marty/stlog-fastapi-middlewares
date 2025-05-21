UV=uv
UV_RUN=$(UV) run
FIX=1

.PHONY: lint
lint: ## Lint the code
ifeq ($(FIX), 1)
	$(UV_RUN) ruff check --fix .
	$(UV_RUN) ruff format .
else
	$(UV_RUN) ruff check .
	$(UV_RUN) ruff format --check .
endif
	$(UV_RUN) mypy --check-untyped-defs .

.PHONY: test
test: ## Test the code
	$(UV_RUN) pytest .

.PHONY: clean
clean: ## Clean the repository
	rm -Rf .venv .*_cache build dist htmlcov 
	find . -type d -name __pycache__ -exec rm -Rf {} \; 2>/dev/null || true
	rm -Rf bin/vector vector_installer tmp_vector

.PHONY: no-dirty
no-dirty: ## Check that the repository is clean
	if test -n "$$(git status --porcelain)"; then \
		echo "***** git status *****"; \
		git status; \
		echo "***** git diff *****"; \
		git diff; \
		echo "ERROR: the repository is dirty"; \
		exit 1; \
	fi

.PHONY: doc
doc: ## Generate the documentation
	$(UV_RUN) jinja-tree .

.PHONY: help
help:
	@# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
