"""
Test the recipe agent using Scenario framework.
"""
import os
import warnings
import pytest
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

DEFAULT_CRITERIA = [
    "Agent should not ask more than two follow-up questions",
    "Agent should generate a recipe",
    "Recipe should include a list of ingredients",
    "Recipe should include step-by-step cooking instructions",
    "Recipe should be vegetarian and not include any sort of meat",
]


def _create_agent():
    """Create recipe agent based on configuration."""
    if USE_CUSTOM_GATEWAY:
        return create_custom_gateway_agent(model=AGENT_MODEL)
    return create_openai_agent(model=AGENT_MODEL)


def _get_failure_message(result):
    """Format failure message from scenario result."""
    if hasattr(result, 'results') and result.results:
        results = result.results
        msg = "Scenario failed:\n"
        if hasattr(results, 'unmet_criteria') and results.unmet_criteria:
            msg += f"Unmet criteria: {', '.join(results.unmet_criteria)}\n"
        if hasattr(results, 'reasoning') and results.reasoning:
            msg += f"Reasoning: {results.reasoning}"
        return msg
    return f"Scenario failed: {result.failure_reason if hasattr(result, 'failure_reason') else 'Unknown reason'}"


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
    """Test basic vegetarian recipe request."""
    agent = _create_agent()
    result = await scenario.run(
        name="vegetarian recipe request",
        description="""
            It's Saturday evening, the user is very hungry and tired,
            but has no money to order out, so they are looking for a recipe.
            The user wants something quick and easy to make.
        """,
        agents=[
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(model=JUDGE_MODEL, criteria=DEFAULT_CRITERIA),
        ],
        max_turns=5,
    )
    assert result.success, _get_failure_message(result)


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_recipe_agent_handles_follow_up():
    """Test agent handles follow-up questions appropriately."""
    agent = _create_agent()
    result = await scenario.run(
        name="recipe follow-up question",
        description="User asks for a recipe, then asks about substitutions.",
        agents=[
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(model=JUDGE_MODEL, criteria=DEFAULT_CRITERIA),
        ],
        max_turns=4,
    )
    assert result.success, _get_failure_message(result)


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_recipe_with_specific_cuisine():
    """Test recipe request for specific cuisine type."""
    agent = _create_agent()
    result = await scenario.run(
        name="specific cuisine recipe",
        description="User wants an Italian vegetarian recipe.",
        agents=[
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(model=JUDGE_MODEL, criteria=DEFAULT_CRITERIA),
        ],
        max_turns=5,
    )
    assert result.success, _get_failure_message(result)


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_recipe_with_dietary_restrictions():
    """Test recipe request with specific dietary restrictions."""
    agent = _create_agent()
    criteria = DEFAULT_CRITERIA + [
        "Recipe should accommodate dietary restrictions mentioned by user",
    ]
    result = await scenario.run(
        name="dietary restrictions recipe",
        description="User wants a gluten-free vegetarian recipe.",
        agents=[
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(model=JUDGE_MODEL, criteria=criteria),
        ],
        max_turns=5,
    )
    assert result.success, _get_failure_message(result)


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_recipe_with_time_constraint():
    """Test recipe request with time constraint."""
    agent = _create_agent()
    result = await scenario.run(
        name="quick recipe request",
        description="User needs a recipe that can be made in under 20 minutes.",
        agents=[
            agent,
            scenario.UserSimulatorAgent(model=USER_SIMULATOR_MODEL),
            scenario.JudgeAgent(model=JUDGE_MODEL, criteria=DEFAULT_CRITERIA),
        ],
        max_turns=5,
    )
    assert result.success, _get_failure_message(result)

