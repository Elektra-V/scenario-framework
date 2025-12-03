# Quick Start: Setting Up CI Pipeline Securely

## 🎯 Goal
Set up GitLab CI to run your pytest Scenario tests without exposing API keys.

## ✅ Step 1: Add Variables in GitLab

1. Open your GitLab project
2. Go to **Settings** → **CI/CD** → **Variables** (expand section)
3. Click **Add variable**

## ✅ Step 2: Add Required Variables

### If Using Custom Gateway:

Add these variables (one at a time):

| Variable Name | Value | Protect? | Mask? |
|--------------|-------|----------|-------|
| `USE_CUSTOM_GATEWAY` | `true` | ✅ | ❌ |
| `CUSTOM_GATEWAY_API_KEY` | Your API key | ✅ | ✅ |
| `CUSTOM_GATEWAY_BASE_URL` | Your gateway URL | ✅ | ❌ |
| `GENAI_USERNAME` | Your username | ✅ | ✅ |
| `GENAI_PASSWORD` | Your password | ✅ | ✅ |
| `CUSTOM_MODEL` | `Llama-3.3-70B-Instruct` | ✅ | ❌ |

### If Using OpenAI:

| Variable Name | Value | Protect? | Mask? |
|--------------|-------|----------|-------|
| `OPENAI_API_KEY` | `sk-...` | ✅ | ✅ |

### Optional Variables:

| Variable Name | Value | Protect? | Mask? |
|--------------|-------|----------|-------|
| `USER_SIMULATOR_MODEL` | `gpt-4o-mini` | ❌ | ❌ |
| `JUDGE_MODEL` | `gpt-4o` | ❌ | ❌ |
| `LANGWATCH_API_KEY` | Your key | ✅ | ✅ |
| `LANGWATCH_ENDPOINT` | `https://app.langwatch.ai` | ❌ | ❌ |

## ✅ Step 3: Test the Pipeline

1. Go to **CI/CD** → **Pipelines**
2. Click **Run pipeline**
3. Select your branch (usually `main`)
4. Watch it run!

## 🔒 Security Checklist

- [ ] All API keys added as CI/CD Variables
- [ ] Sensitive variables marked as **Protected**
- [ ] Sensitive variables marked as **Masked**
- [ ] No secrets in `.gitlab-ci.yml` file
- [ ] No secrets in code files
- [ ] `.env` file is in `.gitignore` ✅ (already done)

## ❓ Troubleshooting

**Pipeline fails: "API key not found"**
- Check variable name matches exactly (case-sensitive)
- Verify variable is set (go to Variables page)
- Check if variable is Protected but branch is not protected

**Variables not masked in logs**
- Some error messages might show values
- This is normal - GitLab masks them in most places
- Check that "Mask variable" is checked

**Need more help?**
- See `SECURE_SETUP.md` for detailed instructions
- See `CI_SETUP.md` for full documentation

