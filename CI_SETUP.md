# GitLab CI Pipeline Setup

## Overview

The CI pipeline runs pytest tests using the Scenario framework. The pipeline uses `uv` for dependency management and runs tests on the `asprunner` tagged runner.

## Pipeline Jobs

### `test:scenario`
- **Stage**: test
- **Runner**: `asprunner` (tagged)
- **Image**: `python:3.11`
- **Purpose**: Runs all Scenario framework tests
- **Output**: JUnit XML test results

## Required CI/CD Variables

Set these in GitLab CI/CD Settings → Variables:

### For OpenAI (if not using custom gateway):
- `OPENAI_API_KEY` - Your OpenAI API key

### For Custom Gateway:
- `USE_CUSTOM_GATEWAY` - Set to `true` to use custom gateway
- `CUSTOM_GATEWAY_API_KEY` - Gateway API key
- `CUSTOM_GATEWAY_BASE_URL` - Gateway base URL (e.g., `https://genai.iais.fraunhofer.de/api/v2`)
- `GENAI_USERNAME` - Gateway username
- `GENAI_PASSWORD` - Gateway password
- `CUSTOM_MODEL` - Model name (e.g., `Llama-3.3-70B-Instruct`)

### Model Configuration (optional):
- `USER_SIMULATOR_MODEL` - Default: `gpt-4o-mini`
- `JUDGE_MODEL` - Default: `gpt-4o`

### LangWatch (optional - for visualization):
- `LANGWATCH_API_KEY` - LangWatch API key
- `LANGWATCH_ENDPOINT` - Default: `https://app.langwatch.ai`

## Setting Up CI/CD Variables Securely

**⚠️ IMPORTANT: Never hardcode API keys in code or YAML files!**

### Step-by-Step Setup:

1. Go to your GitLab project
2. Navigate to **Settings → CI/CD → Variables**
3. Click **Add variable** for each required variable

### For Each Variable:

**For API Keys and Passwords (Sensitive):**
- ✅ **Protect variable**: Check this (only available on protected branches)
- ✅ **Mask variable**: Check this (masks value in CI logs)
- ✅ **Expand variable reference**: Check this

**For Non-Sensitive Values (URLs, model names):**
- ❌ **Protect variable**: Optional
- ❌ **Mask variable**: Not needed
- ✅ **Expand variable reference**: Check this

### Security Best Practices:

- ✅ All secrets stored as CI/CD Variables (not in code)
- ✅ Sensitive variables marked as **Protected** and **Masked**
- ✅ `.env` file is in `.gitignore` (already configured)
- ✅ Never commit real API keys to the repository
- ✅ Use different keys for different environments if needed

See `SECURE_SETUP.md` for detailed step-by-step instructions with screenshots guidance.

## Pipeline Behavior

- **Triggers**: Runs on pushes to `main`, `develop`, and merge requests
- **Cache**: Caches pip cache and `.venv/` directory for faster builds
- **Artifacts**: Test results are saved as JUnit XML for GitLab integration
- **Timeout**: Each test has a 5-minute timeout (configured in `pyproject.toml`)

## Manual Pipeline Run

To manually trigger the pipeline:
1. Go to **CI/CD → Pipelines**
2. Click **Run pipeline**
3. Select branch (usually `main` or `develop`)

## Troubleshooting

### Tests fail with "API key not found"
- Ensure all required CI/CD variables are set
- Check that variables are not masked incorrectly
- Verify variable names match exactly (case-sensitive)

### Tests timeout
- Check if API endpoints are accessible from CI runner
- Verify network connectivity
- Consider increasing timeout in `pyproject.toml` if needed

### Runner not found
- Ensure `asprunner` tag exists on your GitLab runner
- Check runner is active and can access the Docker image `python:3.11`

## Local Testing Before CI

Test locally before pushing:

```bash
# Set environment variables (or use .env file)
export USE_CUSTOM_GATEWAY=true
export CUSTOM_GATEWAY_API_KEY=your_key
# ... etc

# Run tests exactly as CI does
uv run pytest tests/ -v --tb=short --junit-xml=test-results.xml
```
