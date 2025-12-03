# CI Pipeline Setup Guide

This document explains how to set up and run the pytest test suite locally and in GitLab CI.

## Files Added for CI Integration

### 1. `pyproject.toml` - Pytest Configuration
- Added `[tool.pytest.ini_options]` section
- Configured test paths, markers, and timeout settings
- Added `pytest-timeout` dependency

### 2. `tests/conftest.py` - Shared Fixtures
- Contains reusable pytest fixtures for all tests
- Handles LangWatch configuration
- Provides fixtures: `recipe_agent`, `default_criteria`, `judge_model`, etc.

### 3. `tests/test_recipe_scenario.py` - Refactored Tests
- Organized into `TestVegetarianRecipeAgent` class
- Uses fixtures from `conftest.py`
- Contains 3 test scenarios

### 4. `.gitlab-ci.yml` - GitLab CI Configuration
- Defines test job that runs pytest
- Configures environment variables
- Generates JUnit XML reports

## Local Testing

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Specific Test
```bash
uv run pytest tests/test_recipe_scenario.py::TestVegetarianRecipeAgent::test_basic_recipe_request -v
```

### Run Tests with Markers
```bash
uv run pytest tests/ -m scenario -v
```

### Run Tests with Timeout
```bash
uv run pytest tests/ --timeout=300 -v
```

## GitLab CI Setup

### Step 1: Configure CI/CD Variables

In GitLab: **Settings → CI/CD → Variables**

Add these variables (mark sensitive ones as "Masked" and "Protected"):

| Variable Name | Example Value | Masked | Protected |
|--------------|---------------|--------|-----------|
| `USE_CUSTOM_GATEWAY` | `true` | No | No |
| `CUSTOM_GATEWAY_API_KEY` | `xxxx` | Yes | Yes |
| `CUSTOM_GATEWAY_BASE_URL` | `https://genai.iais.fraunhofer.de/api/v2` | No | Yes |
| `GENAI_USERNAME` | `your-username` | Yes | Yes |
| `GENAI_PASSWORD` | `your-password` | Yes | Yes |
| `CUSTOM_MODEL` | `Llama-3.3-70B-Instruct` | No | No |
| `OPENAI_API_KEY` | `your-openai-key` | Yes | Yes |
| `USER_SIMULATOR_MODEL` | `gpt-4o-mini` | No | No |
| `JUDGE_MODEL` | `gpt-4o` | No | No |
| `LANGWATCH_API_KEY` | `your-langwatch-key` | Yes | Yes |
| `LANGWATCH_ENDPOINT` | `https://app.langwatch.ai` | No | No |

### Step 2: Push to GitLab

The `.gitlab-ci.yml` file is already in the repo. When you push to GitLab, the pipeline will automatically run.

### Step 3: Monitor Pipeline

- Go to **CI/CD → Pipelines** in GitLab
- View test results and artifacts
- Check JUnit XML reports for detailed test results

## Test Structure

### Test Suites
- `TestVegetarianRecipeAgent` - Main test class
  - `test_basic_recipe_request` - Basic recipe scenario
  - `test_recipe_with_follow_up_question` - Follow-up question scenario
  - `test_recipe_with_specific_cuisine` - Specific cuisine scenario

### Fixtures Available
- `recipe_agent` - Creates RecipeAgent instance
- `default_criteria` - Default judge criteria
- `user_simulator_model` - User simulator model name
- `judge_model` - Judge model name
- `agent_model` - Agent model name
- `use_custom_gateway` - Boolean for gateway usage

## Troubleshooting

### Tests fail locally
1. Check `.env` file has all required variables
2. Verify API keys are valid
3. Run `uv run pytest tests/ -v` to see detailed output

### CI Pipeline fails
1. Check CI/CD variables are set correctly
2. Verify all required variables are configured
3. Check pipeline logs for specific errors
4. Ensure GitLab Runner has network access to your gateway

### Timeout errors
- Tests have 5-minute timeout (300 seconds)
- Increase timeout in `pyproject.toml` if needed:
  ```toml
  timeout = 600  # 10 minutes
  ```

## Next Steps

1. **Test locally first**: Run `uv run pytest tests/ -v` on your work machine
2. **Verify all tests pass**: Ensure all 3 tests succeed
3. **Push to GitLab**: Commit and push changes
4. **Configure CI variables**: Add all required variables in GitLab
5. **Monitor pipeline**: Check CI/CD → Pipelines for results

