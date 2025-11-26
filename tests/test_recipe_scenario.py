"""
Test the recipe agent using Scenario framework.
"""
import os
import pytest
import scenario
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agent factory
from agents.recipe_agent import create_openai_agent, create_custom_gateway_agent


# ============================================================================
# CONFIGURATION: Switch between OpenAI and custom gateway
# ============================================================================
USE_CUSTOM_GATEWAY = os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "llama-3-70b")  # Your gateway model


@pytest.mark.asyncio
async def test_vegetarian_recipe_agent():
    """
    Test that the recipe agent provides vegetarian recipes correctly.
    """
    # Create agent based on configuration
    if USE_CUSTOM_GATEWAY:
        agent = create_custom_gateway_agent(model=CUSTOM_MODEL)
    else:
        agent = create_openai_agent(model="gpt-4o-mini")
    
    # Run the scenario
    result = await scenario.run(
        name="vegetarian recipe request",
        description="""
            It's Saturday evening, the user is very hungry and tired,
            but has no money to order out, so they are looking for a recipe.
            The user wants something quick and easy to make.
        """,
        agents=[
            agent,  # Agent under test
            scenario.UserSimulatorAgent(
                model="gpt-4o-mini",  # User simulator can use different model
            ),
            scenario.JudgeAgent(
                model="gpt-4o-mini",  # Judge can use different model
                criteria=[
                    "Agent asks at most one follow-up question",
                    "Agent provides a vegetarian recipe",
                    "Recipe includes a list of ingredients",
                    "Recipe includes step-by-step cooking instructions",
                    "Recipe does not include any meat or animal products",
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
        agent = create_custom_gateway_agent(model=CUSTOM_MODEL)
    else:
        agent = create_openai_agent(model="gpt-4o-mini")
    
    result = await scenario.run(
        name="recipe follow-up question",
        description="User asks for a recipe, then asks about substitutions.",
        agents=[
            agent,
            scenario.UserSimulatorAgent(model="gpt-4o-mini"),
            scenario.JudgeAgent(
                model="gpt-4o-mini",
                criteria=[
                    "Agent provides a recipe",
                    "Agent handles substitution question appropriately",
                ],
            ),
        ],
        max_turns=4,
    )
    
    assert result.success

