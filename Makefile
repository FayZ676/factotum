help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

install: ## Set up development environment
	python -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

# Testing

test_post: ## Test post command with last 5 commits
	python -m src.cli post --last=5

test_commit: ## Test commit command
	python -m src.cli commit

test_all: test_post test_commit ## Run all tests

# Hooks

install_hook: ## Install git pre-push hook
	cp hooks/pre-push .git/hooks/pre-push
	chmod +x .git/hooks/pre-push

uninstall_hook: ## Remove git pre-push hook
	rm -f .git/hooks/pre-push

# Binary Commands

build_binary: ## Build the executable binary
	pyinstaller --onefile --name gitscribe main.py

test_binary: ## Test the built binary
	./dist/gitscribe post --last 1
	./dist/gitscribe commit

install_binary: build_binary ## Install binary to system PATH
	sudo cp dist/gitscribe /usr/local/bin/
	sudo chmod +x /usr/local/bin/gitscribe 	

uninstall: ## Remove binary from system PATH and configuration
	sudo rm -f /usr/local/bin/gitscribe
	rm -rf ~/.gitscribe