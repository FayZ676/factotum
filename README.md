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

### Uninstall

**macOS/Linux:**
```bash
sudo rm /usr/local/bin/fac
rm -rf ~/.config/factotum
```

**Windows (PowerShell):**
```powershell
Remove-Item "$env:USERPROFILE\fac.exe"
Remove-Item -Recurse -Force "$env:USERPROFILE\.config\factotum"
# If you added it to a directory in your PATH, remove it from there instead
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
