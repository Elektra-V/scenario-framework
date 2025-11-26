# Installation Guide

This guide covers installation on different platforms.

## Quick Start (All Platforms)

```bash
# Clone or copy the project
cd test_agent

# Run the setup script
./setup.sh

# Edit .env file with your API keys
nano .env  # or use your preferred editor

# Run tests
uv run pytest -q
```

## Platform-Specific Instructions

### Ubuntu/Debian Linux

#### Prerequisites

```bash
# Update package list
sudo apt-get update

# Install curl (if not already installed)
sudo apt-get install -y curl

# Install build essentials (for some Python packages)
sudo apt-get install -y build-essential
```

#### Installation

```bash
# Option 1: Use the setup script (recommended)
./setup.sh

# Option 2: Manual installation
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"

# Initialize project
uv init -p 3.11 --no-readme

# Install dependencies
uv add langwatch-scenario openai pytest pytest-asyncio python-dotenv

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

#### Adding uv to PATH (Permanent)

Add this to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

### macOS

#### Prerequisites

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Installation

```bash
# Option 1: Use the setup script (recommended)
./setup.sh

# Option 2: Manual installation with Homebrew
brew install uv

# Initialize project
uv init -p 3.11 --no-readme

# Install dependencies
uv add langwatch-scenario openai pytest pytest-asyncio python-dotenv

# Create .env file
cp .env.example .env
# Edit .env with your API keys
```

### Windows (WSL2 / Git Bash)

If using WSL2 (Windows Subsystem for Linux), follow the Ubuntu instructions above.

For native Windows, you can use Git Bash:

```bash
# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Then follow similar steps as Linux
uv init -p 3.11 --no-readme
uv add langwatch-scenario openai pytest pytest-asyncio python-dotenv
cp .env.example .env
```

## Verification

After installation, verify everything works:

```bash
# Check uv is installed
uv --version

# Check Python version
uv run python --version

# Test imports
uv run python -c "import scenario; import openai; print('✅ All imports successful')"

# List available models (requires API keys in .env)
uv run python list_models.py
```

## Troubleshooting

### uv not found after installation

**Linux/macOS:**
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

Add to your shell config file (`~/.bashrc`, `~/.zshrc`, etc.) for permanent fix.

### Python version issues

uv will automatically download and use Python 3.11+ if needed. No manual Python installation required.

### Permission denied on setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

### Network issues on cluster

If you're behind a corporate firewall or proxy:

```bash
# Set proxy environment variables
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080

# Then run setup
./setup.sh
```

### Missing system dependencies (Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y curl build-essential libssl-dev
```

## Environment Variables

Make sure your `.env` file contains:

**For OpenAI (local testing):**
```bash
OPENAI_API_KEY=your_key_here
```

**For Custom Gateway:**
```bash
USE_CUSTOM_GATEWAY=true
CUSTOM_GATEWAY_API_KEY=xxxx
CUSTOM_GATEWAY_BASE_URL=https://genai.iais.fraunhofer.de/api/v2
GENAI_USERNAME=your_username
GENAI_PASSWORD=your_password
CUSTOM_MODEL=Llama-3-SauerkrautLM
```

## Next Steps

After installation:

1. **Configure environment**: Edit `.env` with your API keys
2. **Test connection**: Run `uv run python list_models.py`
3. **Run tests**: Run `uv run pytest -q`
4. **Run scenario**: Run `uv run python run_scenario.py`

For more details, see [README.md](README.md).

