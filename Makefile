PROJECT_NAME := core
ASGI_APP := $(PROJECT_NAME).asgi:application
HOST := 127.0.0.1
PORT := 8000

.DEFAULT_GOAL := help

.PHONY: help
help: ## Display this help
	@echo "Available make commands:"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install dependencies from requirements.txt
	pip install -r requirements.txt

.PHONY: run
run: ## Run Django app with Uvicorn
	uvicorn $(ASGI_APP) --host $(HOST) --port $(PORT) --reload

.PHONY: migrate
migrate: ## Apply database migrations
	python manage.py migrate

.PHONY: makemigrations
makemigrations: ## Create new migrations based on model changes
	python manage.py makemigrations

.PHONY: collectstatic
collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

.PHONY: test
test: ## Run Django tests
	python manage.py test

.PHONY: clean
clean: ## Clean up unnecessary cached files
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -rf {} +

