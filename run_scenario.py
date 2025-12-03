"""
Standalone script to run a scenario outside of pytest.
Useful for debugging and interactive testing.
"""
import asyncio
import os
import sys
import warnings
from contextlib import redirect_stderr
from io import StringIO
from dotenv import load_dotenv
import scenario
from agents.recipe_agent import create_openai_agent, create_custom_gateway_agent

load_dotenv()

LANGWATCH_API_KEY = os.getenv("LANGWATCH_API_KEY")
LANGWATCH_ENDPOINT = os.getenv("LANGWATCH_ENDPOINT", "https://app.langwatch.ai")
LANGWATCH_ENABLED = bool(LANGWATCH_API_KEY)

if not LANGWATCH_ENABLED:
    os.environ.setdefault("LANGWATCH_DISABLE_EVENTS", "true")
    warnings.filterwarnings("ignore", category=UserWarning)
else:
    try:
        scenario.configure(
            langwatch_api_key=LANGWATCH_API_KEY,
            langwatch_endpoint=LANGWATCH_ENDPOINT,
        )
    except Exception:
        os.environ.setdefault("LANGWATCH_DISABLE_EVENTS", "true")

USE_CUSTOM_GATEWAY = os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "Llama-3.3-70B-Instruct")
AGENT_MODEL = CUSTOM_MODEL if USE_CUSTOM_GATEWAY else "gpt-4o-mini"
USER_SIMULATOR_MODEL = os.getenv("USER_SIMULATOR_MODEL", "gpt-4o-mini")
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "gpt-4o")


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "═" * 70)
    print(f"  {title}")
    print("═" * 70)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print("─" * 70)


def print_info(label: str, value: str):
    """Print formatted info line."""
    print(f"  {label:.<30} {value}")


async def main():
    """Run a single scenario interactively."""
    print("\033[2J\033[H", end="")
    print_header("🍳 Recipe Agent Scenario Test")
    
    print_section("Configuration")
    if USE_CUSTOM_GATEWAY:
        print_info("Agent Model", f"{AGENT_MODEL} (Gateway)")
    else:
        print_info("Agent Model", f"{AGENT_MODEL} (OpenAI)")
    print_info("User Simulator Model", USER_SIMULATOR_MODEL)
    print_info("Judge Model", JUDGE_MODEL)
    if LANGWATCH_ENABLED:
        print_info("LangWatch", f"✅ Enabled")
        print_info("LangWatch Endpoint", LANGWATCH_ENDPOINT)
    else:
        print_info("LangWatch", "⚠️  Disabled (set LANGWATCH_API_KEY to enable)")
    
    if USE_CUSTOM_GATEWAY:
        agent = create_custom_gateway_agent(model=AGENT_MODEL)
    else:
        agent = create_openai_agent(model=AGENT_MODEL)
    
    print_section("Running Scenario")
    print("  Starting conversation simulation...\n")
    
    scenario_config = {
        "name": "vegetarian recipe request",
        "description": """
            It's Saturday evening, the user is very hungry and tired,
            but has no money to order out, so they are looking for a recipe.
            The user wants something quick and easy to make.
        """,
        "agents": [
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(
                model=JUDGE_MODEL,
                criteria=[
                    "Agent should not ask more than two follow-up questions",
                    "Agent should generate a recipe",
                    "Recipe should include a list of ingredients",
                    "Recipe should include step-by-step cooking instructions",
                    "Recipe should be vegetarian and not include any sort of meat",
                ],
            ),
        ],
        "max_turns": 5,
    }
    
    if not LANGWATCH_ENABLED:
        stderr_capture = StringIO()
        with redirect_stderr(stderr_capture):
            result = await scenario.run(**scenario_config)
    else:
        result = await scenario.run(**scenario_config)
    
    print_section("Results")
    
    if result.success:
        print("\n  ✅ SUCCESS - All criteria met!")
    else:
        print("\n  ❌ FAILED - Some criteria not met")
        
        if hasattr(result, 'failure_reason') and result.failure_reason:
            print(f"\n  Failure Reason: {result.failure_reason}")
        elif hasattr(result, 'results') and result.results:
            results = result.results
            
            if hasattr(results, 'met_criteria') and results.met_criteria:
                print("\n  ✅ Met Criteria:")
                for criterion in results.met_criteria:
                    print(f"     • {criterion}")
            
            if hasattr(results, 'unmet_criteria') and results.unmet_criteria:
                print("\n  ❌ Unmet Criteria:")
                for criterion in results.unmet_criteria:
                    print(f"     • {criterion}")
            
            if hasattr(results, 'reasoning') and results.reasoning:
                print(f"\n  📝 Judge Reasoning:")
                reasoning_lines = results.reasoning.split('. ')
                for line in reasoning_lines:
                    if line.strip():
                        print(f"     {line.strip()}")
        else:
            print("\n  ⚠️  Failure reason: Unknown")
    
    print("\n" + "═" * 70 + "\n")
    
    return result.success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

