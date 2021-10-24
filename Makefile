help:
	@echo "venv"
	@echo "install"

.PHONY: dev
dev:
	python3 -m venv .venv
	. .venv/bin/activate && python3 -m pip install --upgrade pip
	. .venv/bin/activate && python3 -m pip install --editable .[dev]

.PHONY: format
format:
	black cfgmgr
	isort cfgmgr

.PHONY: lint
lint:
	pylint cfgmgr
