# Factotum

> _**Factotum** - /fakˈtōdəm/_
> 
> _A person who does all kinds of work._

## Demo

1. Using the preconfigured `commit-message` action to automatically generate a commit message for staged staged code changes.

https://github.com/user-attachments/assets/b918a8e5-d857-4c33-9891-d6e186e329b8

2. Using the preconfigured `commit-summary` action to generate a twitter post about past commits.

https://github.com/user-attachments/assets/873b649e-fb89-45c2-950c-96437d244405

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

1. `commit-summary`: Look at all commit messages in some block of time and use a LLM to summarize them.
2. `commit-message`: Look at staged code changes and use a LLM to generate a clear and professional commit message.

### Creating Custom Actions

Edit `~/.factotum/config.json` to add your own actions. Each action can have multiple steps that either run shell commands or call the LLM.

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

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
