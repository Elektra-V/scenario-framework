# Recipe Agent Testing with Scenario

This project demonstrates how to test an AI agent using the Scenario framework, with support for both OpenAI and custom gateway backends.

## Quick Start

```bash
# Run the setup script (works on macOS and Linux)
./setup.sh

# Edit .env file with your API keys
nano .env  # or use your preferred editor

# Run tests
uv run pytest -q
```

## Setup

### Prerequisites

- Python 3.11+ (uv will install it automatically if needed)
- [uv](https://github.com/astral-sh/uv) package manager (setup script installs it)

### Installation

**Option 1: Automated Setup (Recommended)**

```bash
# Run the setup script
./setup.sh
```

The setup script will:
- Detect your OS (macOS/Linux)
- Install uv if needed
- Initialize the project
- Install all dependencies
- Create `.env` from `.env.example`

**Option 2: Manual Setup**

**macOS:**
```bash
brew install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Ubuntu/Debian:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"  # Add to ~/.bashrc for permanent
```

Then:
```bash
uv init -p 3.11 --no-readme
uv add langwatch-scenario openai pytest pytest-asyncio python-dotenv
cp .env.example .env
# Edit .env and add your API keys
```

For detailed platform-specific instructions, see [INSTALL.md](INSTALL.md).

## Usage

### Using OpenAI (Local Testing)

By default, the tests use OpenAI. Just set `OPENAI_API_KEY` in your `.env`:

```bash
uv run pytest -q
```

### Using Custom Gateway (Company Environment)

The gateway client is already implemented! Your gateway is OpenAI-compatible with Basic Authentication.

1. **Configure environment**:
   ```bash
   # In .env file:
   USE_CUSTOM_GATEWAY=true
   CUSTOM_GATEWAY_API_KEY=xxxx  # Can be placeholder
   CUSTOM_GATEWAY_BASE_URL=https://genai.iais.fraunhofer.de/api/v2
   GENAI_USERNAME=my-username
   GENAI_PASSWORD=my-password
   CUSTOM_MODEL=Llama-3-SauerkrautLM  # or whatever model your gateway uses
   ```

2. **Run tests**:
   ```bash
   uv run pytest -q
   ```

## Project Structure

```
test_agent/
├── pyproject.toml          # uv project config
├── .env.example            # Environment template
├── README.md               # This file
├── INSTALL.md              # Detailed installation guide
├── setup.sh                # Automated setup script
├── Makefile                # Convenient make commands
├── run_scenario.py         # Standalone script to run scenarios
├── list_models.py          # Script to list available models
├── agents/
│   ├── __init__.py
│   └── recipe_agent.py     # Agent implementation (OpenAI + gateway)
└── tests/
    ├── __init__.py
    └── test_recipe_scenario.py  # Scenario tests
```

## How It Works

1. **Agent Adapter**: The `RecipeAgent` class implements `scenario.AgentAdapter`, which is the interface Scenario expects.

2. **Gateway Abstraction**: The agent can switch between OpenAI and your custom gateway via the `use_custom_gateway` flag.

3. **Scenario Testing**: Tests use `scenario.run()` with:
   - Your agent (under test)
   - `UserSimulatorAgent` (simulates user behavior)
   - `JudgeAgent` (evaluates against criteria)

4. **Simulation Loop**: 
   - User simulator generates a message
   - Your agent responds
   - Judge evaluates
   - Loop continues until judge decides success/failure

## Customizing for Your Gateway

The gateway client (`CustomGatewayClient`) is already implemented and uses:
- OpenAI-compatible SDK with Basic Authentication
- Base64-encoded username:password for Authorization header
- Support for `extra_headers` and `extra_body` parameters

The implementation matches your gateway's API structure. Just configure the environment variables:
- `GENAI_USERNAME` and `GENAI_PASSWORD` for Basic Auth
- `CUSTOM_GATEWAY_BASE_URL` for your gateway endpoint
- `CUSTOM_MODEL` for the model identifier
- Set `USE_CUSTOM_GATEWAY=true` to enable it

## Running Tests

```bash
# Run all tests
uv run pytest -q

# Run with verbose output
uv run pytest -v

# Run specific test
uv run pytest tests/test_recipe_scenario.py::test_vegetarian_recipe_agent

# Run scenario standalone (outside pytest, useful for debugging)
uv run python run_scenario.py

# List available models from gateway (chat and embedding models)
uv run python list_models.py
```

## Using Make Commands

For convenience, you can use make commands:

```bash
make setup        # Run automated setup
make install      # Install/update dependencies
make test         # Run tests
make test-verbose # Run tests with verbose output
make list-models  # List available models
make run-scenario # Run scenario standalone
make clean        # Clean temporary files
make help         # Show all available commands
```

## Portability

This project is designed to be portable across platforms:

- ✅ **macOS**: Fully supported
- ✅ **Ubuntu/Debian Linux**: Fully supported
- ✅ **Other Linux distributions**: Should work (may need minor adjustments)
- ✅ **Windows WSL2**: Supported (follow Ubuntu instructions)

The setup script (`setup.sh`) automatically detects your OS and installs dependencies accordingly. All paths are relative, making it easy to move the project between machines.

## References

- [Scenario Documentation](https://scenario.langwatch.ai/basics/concepts)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Installation Guide](INSTALL.md) - Detailed platform-specific instructions
