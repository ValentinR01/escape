# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
SHELL := /bin/bash

.PHONY: install
install:
	@echo "${GREEN}Installing dependencies... ${RESET}"
	cd ./services/administration-service && npm install
	cd ./services/tasks-service && python -m venv .venv
	cd ./services/tasks-service && source .venv/bin/activate && pip install -r requirements.txt

migrate-dry:
	@echo "${GREEN}Running migrations... ${RESET}"
	cd ./services/administration-service && npm run migrate:dry

migrate-reset:
	@echo "${YELLOW}Resetting database... ${YELLOW}"
	cd ./services/administration-service && npm run migrate reset

migrate:
	@echo "${GREEN}Running migrations... ${RESET}"
	cd ./services/administration-service && npm run migrate

up:
	@echo "${GREEN}Starting services... ${RESET}"
	docker compose up -d

start: install up migrate

check:
	@echo "${GREEN}Checking source code... ${RESET}"
	cd ./services/administration-service && npm run check:type
	cd ./services/tasks-service && source .venv/bin/activate && mypy .
	cd ./services/tasks-service && source .venv/bin/activate && ruff check .

make freeze:
	cd ./services/tasks-service && source .venv/bin/activate && pip freeze --exclude-editable >> requirements.txt