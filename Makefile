help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

install: ## Set up development environment
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install -e .

# Testing

test_init: ## Test init command
	python main.py init --help

test_summarize: ## Test summarize-commits action (requires config)
	python main.py summarize-commits --since="1 week ago"

test_cli: ## Test CLI help and structure
	python main.py --help

test_all: test_cli test_init ## Run all basic tests

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
	./dist/gitscribe --help
	./dist/gitscribe init --help

install_binary: build_binary ## Install binary to system PATH
	sudo cp dist/gitscribe /usr/local/bin/
	sudo chmod +x /usr/local/bin/gitscribe 	

uninstall: ## Remove binary from system PATH and configuration
	sudo rm -f /usr/local/bin/gitscribe
	rm -rf ~/.gitscribe

# Development

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.spec
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

dev: install ## Setup and run in development mode
	@echo "✅ Development environment ready!"
	@echo "Run: source .venv/bin/activate"