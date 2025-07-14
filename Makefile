
include .env
export

# Python 3.12 required

install:
	uv sync
	uv tool install ruff
	uv tool install httpie

dev:
	fastapi dev app/main.py
#	uv run uvicorn app.main:app --reload
#   python3 -m app.main

lab:
	uvx --from . --with jupyterlab jupyter lab

run:
	uvicorn app.main:app --no-access-log

image:
	docker build -t pydev1 .

run-image:
	docker run -p 8000:8000 pydev1


test:
	echo "Test"

lint:
	uvx ruff check app --fix

check:
	uvx ruff check app

format:
	uvx ruff format app

clean:
	rm -rf .venv __pycache__ .ruff_cache


.PHONY: clean test