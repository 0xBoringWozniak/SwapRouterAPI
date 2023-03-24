VENV := venv

ifeq ($(OS),Windows_NT)
   BIN=$(VENV)/Scripts
else
   BIN=$(VENV)/bin
endif

export PATH := $(BIN):$(PATH)

PROJECT := service
TESTS := tests

IMAGE_NAME := swap_api
CONTAINER_NAME := SWAP_API


# Clean

clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(VENV)


# Setup
.venv:
	python3 -m venv $(VENV)
	pip3 install -r requirements.txt

setup: .venv


# Format

isort_fix: .venv
	isort $(PROJECT) $(TESTS)

format: isort_fix


# Lint

isort: .venv
	isort --check $(PROJECT) $(TESTS)

flake: .venv
	flake8 $(PROJECT) $(TESTS)

mypy: .venv
	mypy $(PROJECT) $(TESTS)

pylint: .venv
	pylint $(PROJECT) --disable=C0116,C0115,C0114,C0301

lint: isort flake mypy pylint


# Test

.pytest:
	pytest

test: .venv .pytest


# Docker

build:
	docker build . -t $(IMAGE_NAME)

run: build
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker run -p 8000:8000 --env-file=env.txt --name $(CONTAINER_NAME) -d $(IMAGE_NAME)

# All
dev: setup format lint test
all: setup format lint test run

.DEFAULT_GOAL = all