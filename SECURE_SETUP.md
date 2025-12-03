# Secure API Key Setup for GitLab CI

## Overview

Never hardcode API keys in your code or YAML files. GitLab provides secure ways to manage secrets through **CI/CD Variables**.

## Step-by-Step Secure Setup

### 1. Navigate to CI/CD Variables

1. Go to your GitLab project
2. Click **Settings** → **CI/CD**
3. Expand **Variables** section
4. Click **Add variable**

### 2. Add Each Variable Securely

For each API key/secret, follow these steps:

#### Required Variables (choose one option):

**Option A - OpenAI Setup:**
- **Key**: `OPENAI_API_KEY`
- **Value**: `sk-...` (your OpenAI API key)
- **Type**: Variable
- **Environment scope**: All environments
- **Protect variable**: ✅ Check this (only available on protected branches)
- **Mask variable**: ✅ Check this (masks value in logs)
- **Expand variable reference**: ✅ Check this

**Option B - Custom Gateway Setup:**
- **Key**: `USE_CUSTOM_GATEWAY`
- **Value**: `true`
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ❌ (not sensitive)
- **Expand variable reference**: ✅

- **Key**: `CUSTOM_GATEWAY_API_KEY`
- **Value**: Your gateway API key
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ✅
- **Expand variable reference**: ✅

- **Key**: `CUSTOM_GATEWAY_BASE_URL`
- **Value**: `https://your-gateway-url.com/api/v2`
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ❌ (URLs are usually not sensitive)
- **Expand variable reference**: ✅

- **Key**: `GENAI_USERNAME`
- **Value**: Your username
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ✅
- **Expand variable reference**: ✅

- **Key**: `GENAI_PASSWORD`
- **Value**: Your password
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ✅
- **Expand variable reference**: ✅

- **Key**: `CUSTOM_MODEL`
- **Value**: `Llama-3.3-70B-Instruct`
- **Type**: Variable
- **Protect variable**: ✅
- **Mask variable**: ❌ (not sensitive)
- **Expand variable reference**: ✅

#### Optional Variables:

- **Key**: `USER_SIMULATOR_MODEL`
- **Value**: `gpt-4o-mini`
- **Protect variable**: ❌ (optional, not sensitive)
- **Mask variable**: ❌

- **Key**: `JUDGE_MODEL`
- **Value**: `gpt-4o`
- **Protect variable**: ❌ (optional, not sensitive)
- **Mask variable**: ❌

- **Key**: `LANGWATCH_API_KEY`
- **Value**: Your LangWatch API key
- **Protect variable**: ✅
- **Mask variable**: ✅
- **Expand variable reference**: ✅

- **Key**: `LANGWATCH_ENDPOINT`
- **Value**: `https://app.langwatch.ai`
- **Protect variable**: ❌ (optional, not sensitive)
- **Mask variable**: ❌

### 3. Understanding Variable Settings

#### Protect variable
- ✅ **Check this** for sensitive data (API keys, passwords)
- Only available on protected branches/tags
- Prevents accidental exposure on unprotected branches

#### Mask variable
- ✅ **Check this** for secrets (API keys, passwords)
- Masks the value in CI/CD job logs
- Prevents secrets from appearing in pipeline output
- **Note**: GitLab will mask the value, but if it appears in error messages, it might still be visible

#### Expand variable reference
- ✅ **Check this** (recommended)
- Allows variable expansion in other variables
- Useful for building URLs or composite values

### 4. Best Practices

#### ✅ DO:
- Use CI/CD Variables for all secrets
- Mark sensitive variables as **Protected** and **Masked**
- Use different variables for different environments (dev/staging/prod)
- Rotate keys regularly
- Use least privilege (only grant necessary permissions)

#### ❌ DON'T:
- Hardcode secrets in `.gitlab-ci.yml`
- Hardcode secrets in code files
- Commit `.env` files with real secrets
- Share API keys in chat/email
- Use the same key for multiple projects

### 5. Verify Setup

After adding variables:

1. Go to **CI/CD** → **Pipelines**
2. Click **Run pipeline**
3. Select your branch
4. Watch the pipeline run
5. Check that variables are available (but masked in logs)

### 6. Testing Locally

To test with the same setup locally:

1. Create a `.env` file (already in `.gitignore`)
2. Add your variables:
   ```bash
   OPENAI_API_KEY=sk-...
   USE_CUSTOM_GATEWAY=true
   # etc.
   ```
3. Run tests: `uv run pytest tests/`

**Important**: Never commit `.env` file with real secrets!

### 7. Troubleshooting

#### Variables not available in pipeline
- Check variable is not set to "Protected" if running on unprotected branch
- Verify variable name matches exactly (case-sensitive)
- Check environment scope matches your pipeline

#### Masked variables still visible
- Some error messages might show values
- Check job logs carefully
- Consider using file-based secrets for extremely sensitive data

#### Pipeline fails with "API key not found"
- Verify variable name matches what code expects
- Check variable is not accidentally masked incorrectly
- Ensure variable is set for the correct environment scope

## Alternative: File-Based Secrets (Advanced)

For extremely sensitive data, you can use GitLab's file-based secrets:

1. Create a secret file in GitLab
2. Reference it in CI/CD
3. Read it in your script

This is more complex but provides additional security layers.

## Security Checklist

- [ ] All API keys added as CI/CD Variables
- [ ] Sensitive variables marked as Protected
- [ ] Sensitive variables marked as Masked
- [ ] `.env` file in `.gitignore`
- [ ] No secrets in code or YAML files
- [ ] Variables tested in pipeline
- [ ] Access to variables restricted to necessary users

