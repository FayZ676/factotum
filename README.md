# Factotum

> _**Factotum** - /fakˈtōdəm/_
> 
> _A person who does all kinds of work._

Factotum is a CLI tool that lets you create custom commands. Define worflows once in a config file, then execute them as simple commands anywhere on your machine.

## Features

- 🤖 **LLM-Powered Commands** - Create terminal commands that use OpenAI's API for intelligent automation
- ⚙️ **Shell Integration** - Chain shell commands with LLM processing in multi-step workflows
- 🎯 **Git Workflow Automation** - Pre-configured commands for commit messages and commit summaries
- 📋 **Auto-Copy to Clipboard** - Results automatically copied for quick pasting
- 🔧 **Fully Customizable** - Define your own actions with parameters, steps, and prompts

## Quick Start

### Installation

**macOS:**
```bash
curl -L https://github.com/FayZ676/factotum/releases/latest/download/factotum-macos -o /tmp/factotum && chmod +x /tmp/factotum && sudo mv /tmp/factotum /usr/local/bin/fac
```

**Linux:**
```bash
curl -L https://github.com/FayZ676/factotum/releases/latest/download/factotum-linux -o /tmp/factotum && chmod +x /tmp/factotum && sudo mv /tmp/factotum /usr/local/bin/fac
```

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri "https://github.com/FayZ676/factotum/releases/latest/download/factotum-windows.exe" -OutFile "$env:USERPROFILE\fac.exe"
# Add to PATH or move to a directory in your PATH
```

### Initial Setup

1. Initialize configuration with your OpenAI API key:
   ```bash
   fac init
   ```

2. Try the pre-configured commands:
   ```bash
   fac commit-message      # Generate commit message from staged changes
   fac summarize-commits   # Summarize recent commits
   ```

## Usage

### Pre-configured Commands

#### Generate Commit Messages
Automatically create conventional commit messages from your staged changes:

```bash
git add .
fac commit-message
# Output: "feat: Add user authentication with OAuth2" (copied to clipboard)
```

The generated message follows conventional commit format:
- Uses imperative mood
- Includes type prefix (feat:, fix:, docs:, etc.)
- Concise and descriptive

#### Summarize Commits
Get an AI-generated summary of commits in a range:

```bash
fac summarize-commits --commit abc123
# Summarizes all commits from abc123 to HEAD
```

### Creating Custom Actions

Edit `~/.config/factotum/config.json` to add your own actions. Each action can have multiple steps that either run shell commands or call the LLM.

Example structure:
```json
{
  "name": "your-command",
  "description": "What this command does",
  "steps": [
    {
      "name": "step-1",
      "type": "shell",
      "params": [...],
      "value": "echo {{param_name}}"
    },
    {
      "name": "step-2",
      "type": "llm",
      "params": [],
      "value": "Process this: {{@step-1}}"
    }
  ]
}
```

**Step types:**
- `shell`: Execute shell commands
- `llm`: Send prompts to OpenAI's API

**Parameter syntax:**
- `{{param_name}}`: Inject command-line parameters
- `{{@step-name}}`: Inject output from previous steps

## Configuration

Configuration file location: `~/.config/factotum/config.json`

Required fields:
- `openai_api_key`: Your OpenAI API key
- `actions`: Array of action definitions

See [config.json](config.json) for the full template.

## Requirements

- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- Python 3.12+ (for development only; binaries are standalone)

## Development

Clone and set up the development environment:

```bash
git clone https://github.com/FayZ676/factotum.git
cd factotum
make install
```

Run tests:
```bash
make test_all
```

Build binary:
```bash
make build_binary
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
