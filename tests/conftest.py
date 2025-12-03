"""
Shared pytest fixtures for Scenario tests.
"""
import os
import warnings
import pytest
from dotenv import load_dotenv
import scenario
from agents.recipe_agent import create_openai_agent, create_custom_gateway_agent

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


@pytest.fixture(scope="session")
def use_custom_gateway():
    """Fixture to determine if custom gateway should be used."""
    return os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"


@pytest.fixture(scope="session")
def agent_model(use_custom_gateway):
    """Fixture to get the agent model."""
    if use_custom_gateway:
        return os.getenv("CUSTOM_MODEL", "Llama-3.3-70B-Instruct")
    return "gpt-4o-mini"


@pytest.fixture(scope="session")
def user_simulator_model():
    """Fixture to get user simulator model."""
    return os.getenv("USER_SIMULATOR_MODEL", "gpt-4o-mini")


@pytest.fixture(scope="session")
def judge_model():
    """Fixture to get judge model."""
    return os.getenv("JUDGE_MODEL", "gpt-4o")


@pytest.fixture
def recipe_agent(use_custom_gateway, agent_model):
    """Fixture to create recipe agent."""
    if use_custom_gateway:
        return create_custom_gateway_agent(model=agent_model)
    return create_openai_agent(model=agent_model)


@pytest.fixture
def default_criteria():
    """Fixture with default judge criteria."""
    return [
        "Agent should not ask more than two follow-up questions",
        "Agent should generate a recipe",
        "Recipe should include a list of ingredients",
        "Recipe should include step-by-step cooking instructions",
        "Recipe should be vegetarian and not include any sort of meat",
    ]

