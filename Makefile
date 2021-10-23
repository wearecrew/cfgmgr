help:
	@echo "venv"
	@echo "install"

.PHONY: venv
venv:
	python3 -m venv .venv
	. .venv/bin/activate && python3 -m pip install --upgrade pip

.PHONY: install
install:
	python3 -m pip install --editable .[dev]

.PHONY: format
format:
	black .
