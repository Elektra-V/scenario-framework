# Troubleshooting Guide

## Common Errors

### "File or directory not found"

**Possible causes:**

1. **Wrong directory**: Make sure you're in the project root
   ```bash
   cd /Users/vedikachauhan/project/test_agent
   pwd  # Should show: /Users/vedikachauhan/project/test_agent
   ```

2. **Missing .env file**: Create it from the example
   ```bash
   cp .env.example .env
   # Then edit .env with your actual API keys
   ```

3. **Dependencies not installed**: Run
   ```bash
   uv sync
   ```

4. **Python path issues**: Use `uv run` prefix
   ```bash
   # ✅ Correct
   uv run pytest tests/
   
   # ❌ Wrong (if python not in PATH)
   pytest tests/
   ```

## Step-by-Step Setup

1. **Navigate to project directory:**
   ```bash
   cd /Users/vedikachauhan/project/test_agent
   ```

2. **Verify you're in the right place:**
   ```bash
   ls -la
   # Should see: tests/, agents/, pyproject.toml, etc.
   ```

3. **Install/update dependencies:**
   ```bash
   uv sync
   ```

4. **Create .env file (if missing):**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Test collection (no API calls):**
   ```bash
   uv run pytest tests/ --collect-only
   ```

6. **Run tests:**
   ```bash
   uv run pytest tests/ -v
   ```

## Verify Installation

Run these commands to verify everything is set up:

```bash
# Check you're in the right directory
pwd

# Check files exist
ls tests/test_recipe_scenario.py
ls agents/recipe_agent.py
ls pyproject.toml

# Check Python can import
uv run python -c "from agents.recipe_agent import create_openai_agent; print('OK')"

# Check pytest can find tests
uv run pytest tests/ --collect-only
```

## If Still Having Issues

Share the exact command you're running and the full error message.

