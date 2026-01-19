# Installation

This guide covers installing Factotum on macOS, Linux, and Windows, plus manual installation.

## macOS

```bash
curl -L https://github.com/FayZ676/factotum/releases/latest/download/factotum-macos -o /tmp/factotum && chmod +x /tmp/factotum && sudo mv /tmp/factotum /usr/local/bin/
```

## Linux

```bash
curl -L https://github.com/FayZ676/factotum/releases/latest/download/factotum-linux -o /tmp/factotum && chmod +x /tmp/factotum && sudo mv /tmp/factotum /usr/local/bin/
```

## Windows (PowerShell)

```powershell
Invoke-WebRequest -Uri "https://github.com/FayZ676/factotum/releases/latest/download/factotum-windows.exe" -OutFile "$env:USERPROFILE\factotum.exe"
# Then add to PATH or move to a directory in your PATH
```

## Manual Installation

Download the appropriate binary for your platform from the [Releases page](https://github.com/FayZ676/factotum/releases/latest), make it executable, and move it to a directory in your PATH.

## Verify Installation

```bash
factotum --help
```

If the command prints the help text, you’re good to go.


## Next Steps

After installation, run the configuration command to set up your OpenAI API key and default style files:

```bash
fac configure
```

See [USAGE.md](USAGE.md) for detailed configuration instructions and usage examples.
## Uninstall

### Binary Installation

If you installed using the binary installation method:

**macOS/Linux:**

```bash
sudo rm /usr/local/bin/factotum
rm -rf ~/.factotum
```

**Windows:**

```powershell
Remove-Item "$env:USERPROFILE\factotum.exe"
Remove-Item -Recurse -Force "$env:USERPROFILE\.factotum"
# Or remove from wherever you placed it in your PATH
```

### Development Installation

If you installed locally during development:

```bash
make uninstall
```

**Note:** These commands will permanently delete your stored OpenAI API key, default style file configuration, and any other factotum settings. You'll need to reconfigure if you reinstall factotum later.
