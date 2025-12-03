"""
Test the recipe agent using Scenario framework.
"""
import pytest
import scenario


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_vegetarian_recipe_agent(
    recipe_agent, user_simulator_model, judge_model, default_criteria
):
    """
    Test that the recipe agent provides vegetarian recipes correctly.
    """
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
            recipe_agent,  # Agent under test (Llama-3.3-70B-Instruct)
            scenario.UserSimulatorAgent(
                model=user_simulator_model,  # User simulator (gpt-4o-mini)
            ),
            scenario.JudgeAgent(
                model=judge_model,  # Judge agent (gpt-4o for better reasoning)
                criteria=default_criteria,
            ),
        ],
        max_turns=5,  # Limit conversation length
    )
    
    # Assert success
    assert result.success, _get_failure_message(result)


@pytest.mark.scenario
@pytest.mark.asyncio
async def test_recipe_agent_handles_follow_up(
    recipe_agent, user_simulator_model, judge_model, default_criteria
):
    """
    Test that agent handles follow-up questions appropriately.
    """
    result = await scenario.run(
        name="recipe follow-up question",
        description="User asks for a recipe, then asks about substitutions.",
        agents=[
            recipe_agent,  # Agent under test (Llama-3.3-70B-Instruct)
            scenario.UserSimulatorAgent(model=user_simulator_model),
            scenario.JudgeAgent(
                model=judge_model,  # Judge agent (gpt-4o for better reasoning)
                criteria=default_criteria,
            ),
        ],
        max_turns=4,
    )
    
    assert result.success, _get_failure_message(result)


def _get_failure_message(result):
    """Helper to format failure message."""
    if hasattr(result, 'results') and result.results:
        results = result.results
        msg = "Scenario failed:\n"
        if hasattr(results, 'unmet_criteria') and results.unmet_criteria:
            msg += f"Unmet criteria: {', '.join(results.unmet_criteria)}\n"
        if hasattr(results, 'reasoning') and results.reasoning:
            msg += f"Reasoning: {results.reasoning}"
        return msg
    return f"Scenario failed: {result.failure_reason if hasattr(result, 'failure_reason') else 'Unknown reason'}"

