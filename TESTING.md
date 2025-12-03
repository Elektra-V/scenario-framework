# Running Tests Locally

## Prerequisites

1. Ensure you have a `.env` file with required environment variables (copy from `.env.example` if needed)
2. Install dependencies: `uv sync`

## Running Tests

### Run all tests:
```bash
uv run pytest tests/
```

### Run with verbose output:
```bash
uv run pytest tests/ -v
```

### Run only scenario tests:
```bash
uv run pytest tests/ -m scenario
```

### Run a specific test:
```bash
uv run pytest tests/test_recipe_scenario.py::test_vegetarian_recipe_agent
```

### Run tests with output (see print statements):
```bash
uv run pytest tests/ -v -s
```

### Run tests and stop on first failure:
```bash
uv run pytest tests/ -x
```

### Run tests and show coverage:
```bash
uv run pytest tests/ --cov=agents --cov-report=term
```

## Environment Variables

Make sure your `.env` file includes:

**For OpenAI:**
- `OPENAI_API_KEY=your_key_here`

**For Custom Gateway:**
- `USE_CUSTOM_GATEWAY=true`
- `CUSTOM_GATEWAY_API_KEY=your_key`
- `CUSTOM_GATEWAY_BASE_URL=your_gateway_url`
- `GENAI_USERNAME=your_username`
- `GENAI_PASSWORD=your_password`
- `CUSTOM_MODEL=Llama-3.3-70B-Instruct`

**For LangWatch (optional):**
- `LANGWATCH_API_KEY=your_key`
- `LANGWATCH_ENDPOINT=https://app.langwatch.ai`

**Model Configuration:**
- `USER_SIMULATOR_MODEL=gpt-4o-mini` (default)
- `JUDGE_MODEL=gpt-4o` (default)

## Test Timeout

Tests have a 5-minute timeout per test (configured in `pyproject.toml`). If a test takes longer, it will be marked as failed.

