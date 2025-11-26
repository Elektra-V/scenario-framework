"""
Test the recipe agent using Scenario framework.
"""
import os
import warnings
import pytest
import scenario
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangWatch configuration
LANGWATCH_API_KEY = os.getenv("LANGWATCH_API_KEY")
LANGWATCH_ENDPOINT = os.getenv("LANGWATCH_ENDPOINT", "https://app.langwatch.ai")
LANGWATCH_ENABLED = bool(LANGWATCH_API_KEY)

# Only suppress LangWatch if API key is not provided
if not LANGWATCH_ENABLED:
    os.environ.setdefault("LANGWATCH_DISABLE_EVENTS", "true")
    warnings.filterwarnings("ignore", category=UserWarning)
else:
    # Configure LangWatch when API key is available
    try:
        scenario.configure(
            langwatch_api_key=LANGWATCH_API_KEY,
            langwatch_endpoint=LANGWATCH_ENDPOINT,
        )
    except Exception:
        # If configuration fails, fall back to disabled mode
        os.environ.setdefault("LANGWATCH_DISABLE_EVENTS", "true")

# Import agent factory
from agents.recipe_agent import create_openai_agent, create_custom_gateway_agent


# ============================================================================
# CONFIGURATION: Switch between OpenAI and custom gateway
# ============================================================================
USE_CUSTOM_GATEWAY = os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "Llama-3.3-70B-Instruct")  # Gateway model for RecipeAgent

# Model configuration for different agents
# Each agent can use a different model - this is recommended!
AGENT_MODEL = CUSTOM_MODEL if USE_CUSTOM_GATEWAY else "gpt-4o-mini"  # Agent under test
USER_SIMULATOR_MODEL = os.getenv("USER_SIMULATOR_MODEL", "gpt-4o-mini")  # User simulator
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "gpt-4o")  # Judge agent (better reasoning)


@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
    """
    Test that the recipe agent provides vegetarian recipes correctly.
    """
    # Create agent based on configuration
    if USE_CUSTOM_GATEWAY:
        agent = create_custom_gateway_agent(model=AGENT_MODEL)
    else:
        agent = create_openai_agent(model=AGENT_MODEL)
    
    # Run the scenario
    # NOTE: Each agent can use a DIFFERENT model - this is recommended!
    # - RecipeAgent: Uses Llama-3.3-70B-Instruct (gateway) for quality responses
    # - UserSimulatorAgent: Uses gpt-4o-mini (fast, cost-effective)
    # - JudgeAgent: Uses gpt-4o (better reasoning for evaluation)
    result = await scenario.run(
        name="vegetarian recipe request",
        description="""
            It's Saturday evening, the user is very hungry and tired,
            but has no money to order out, so they are looking for a recipe.
            The user wants something quick and easy to make.
        """,
        agents=[
            agent,  # Agent under test (Llama-3.3-70B-Instruct)
            scenario.UserSimulatorAgent(
                model=USER_SIMULATOR_MODEL,  # User simulator (gpt-4o-mini)
            ),
            scenario.JudgeAgent(
                model=JUDGE_MODEL,  # Judge agent (gpt-4o for better reasoning)
                criteria=[
                    "Agent asks at most one follow-up question (a single simple question, not multiple options)",
                    "Agent provides a vegetarian recipe",
                    "Recipe includes a list of ingredients",
                    "Recipe includes step-by-step cooking instructions",
                    "Recipe does not include any meat, fish, dairy (cheese, milk, butter), eggs, honey, or any animal products",
                ],
            ),
        ],
        max_turns=5,  # Limit conversation length
    )
    
    # Assert success
    assert result.success, f"Scenario failed: {result.failure_reason if hasattr(result, 'failure_reason') else 'Unknown reason'}"


@pytest.mark.asyncio
async def test_recipe_agent_handles_follow_up():
    """
    Test that agent handles follow-up questions appropriately.
    """
    if USE_CUSTOM_GATEWAY:
        agent = create_custom_gateway_agent(model=AGENT_MODEL)
    else:
        agent = create_openai_agent(model=AGENT_MODEL)
    
    result = await scenario.run(
        name="recipe follow-up question",
        description="User asks for a recipe, then asks about substitutions.",
        agents=[
            agent,  # Agent under test (Llama-3.3-70B-Instruct)
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(
                model=JUDGE_MODEL,  # Judge agent (gpt-4o for better reasoning)
                criteria=[
                    "Agent provides a recipe",
                    "Recipe does not include any animal products (meat, fish, dairy, eggs, honey)",
                    "Agent handles substitution question appropriately",
                ],
            ),
        ],
        max_turns=4,
    )
    
    assert result.success

