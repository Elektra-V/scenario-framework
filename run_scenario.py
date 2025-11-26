"""
Standalone script to run a scenario outside of pytest.
Useful for debugging and interactive testing.
"""
import asyncio
import os
from dotenv import load_dotenv
import scenario
from agents.recipe_agent import create_openai_agent, create_custom_gateway_agent

# Load environment variables
load_dotenv()

# Configuration
USE_CUSTOM_GATEWAY = os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "Llama-3.3-70B-Instruct")  # Gateway model for RecipeAgent

# Model configuration for different agents
# Each agent can use a different model - this is recommended!
AGENT_MODEL = CUSTOM_MODEL if USE_CUSTOM_GATEWAY else "gpt-4o-mini"  # Agent under test
USER_SIMULATOR_MODEL = os.getenv("USER_SIMULATOR_MODEL", "gpt-4o-mini")  # User simulator
JUDGE_MODEL = os.getenv("JUDGE_MODEL", "gpt-4o")  # Judge agent (better reasoning)


async def main():
    """Run a single scenario interactively."""
    print("=" * 60)
    print("Recipe Agent Scenario Test")
    print("=" * 60)
    
    # Create agent based on configuration
    if USE_CUSTOM_GATEWAY:
        print(f"Using custom gateway with model: {AGENT_MODEL}")
        agent = create_custom_gateway_agent(model=AGENT_MODEL)
    else:
        print(f"Using OpenAI with model: {AGENT_MODEL}")
        agent = create_openai_agent(model=AGENT_MODEL)
    
    print(f"User Simulator Model: {USER_SIMULATOR_MODEL}")
    print(f"Judge Model: {JUDGE_MODEL}")
    print("\nRunning scenario...")
    print("-" * 60)
    
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
    
    # Print results
    print("-" * 60)
    print(f"\nScenario Result: {'✅ SUCCESS' if result.success else '❌ FAILED'}")
    
    if not result.success:
        failure_reason = getattr(result, 'failure_reason', 'Unknown reason')
        print(f"Failure reason: {failure_reason}")
    
    print("=" * 60)
    
    return result.success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)

