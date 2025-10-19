# Development

For detailed development commands, see the `Makefile` in the project root. Key commands include:

## Development Environment

- `make install` - Set up development environment (creates venv and installs dependencies)

## Testing

- `make test_post` - Test post command with last 5 commits
- `make test_commit` - Test commit command
- `make test_all` - Run all tests

## Git Hooks

- `make install_hook` - Install git pre-push hook
- `make uninstall_hook` - Remove git pre-push hook

## Binary Management

- `make build_binary` - Build the executable binary
- `make test_binary` - Test the built binary
- `make install_binary` - Install binary to system PATH
- `make uninstall` - Remove binary from system PATH and configuration

Run `make` or `make help` to see all available targets with descriptions.
