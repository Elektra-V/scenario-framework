"""
Test suite for recipe agent using Scenario framework.
"""
import pytest
import scenario


@pytest.mark.scenario
@pytest.mark.asyncio
class TestVegetarianRecipeAgent:
    """Test suite for vegetarian recipe agent scenarios."""
    
    async def test_basic_recipe_request(
        self, recipe_agent, user_simulator_model, judge_model, default_criteria
    ):
        """Test basic vegetarian recipe request."""
        result = await scenario.run(
            name="basic vegetarian recipe request",
            description="""
                It's Saturday evening, the user is very hungry and tired,
                but has no money to order out, so they are looking for a recipe.
                The user wants something quick and easy to make.
            """,
            agents=[
                recipe_agent,
                scenario.UserSimulatorAgent(model=user_simulator_model),
                scenario.JudgeAgent(
                    model=judge_model,
                    criteria=default_criteria,
                ),
            ],
            max_turns=5,
        )
        
        assert result.success, self._get_failure_message(result)
    
    async def test_recipe_with_follow_up_question(
        self, recipe_agent, user_simulator_model, judge_model, default_criteria
    ):
        """Test recipe request with follow-up question."""
        result = await scenario.run(
            name="recipe follow-up question",
            description="User asks for a recipe, then asks about substitutions.",
            agents=[
                recipe_agent,
                scenario.UserSimulatorAgent(model=user_simulator_model),
                scenario.JudgeAgent(
                    model=judge_model,
                    criteria=default_criteria,
                ),
            ],
            max_turns=4,
        )
        
        assert result.success, self._get_failure_message(result)
    
    async def test_recipe_with_specific_cuisine(
        self, recipe_agent, user_simulator_model, judge_model, default_criteria
    ):
        """Test recipe request for specific cuisine."""
        result = await scenario.run(
            name="specific cuisine recipe",
            description="User wants an Italian vegetarian recipe.",
            agents=[
                recipe_agent,
                scenario.UserSimulatorAgent(model=user_simulator_model),
                scenario.JudgeAgent(
                    model=judge_model,
                    criteria=default_criteria,
                ),
            ],
            max_turns=5,
        )
        
        assert result.success, self._get_failure_message(result)
    
    def _get_failure_message(self, result):
        """Helper to format failure message."""
        if hasattr(result, 'results') and result.results:
            results = result.results
            msg = "Scenario failed:\n"
            if hasattr(results, 'unmet_criteria') and results.unmet_criteria:
                msg += f"Unmet criteria: {', '.join(results.unmet_criteria)}\n"
            if hasattr(results, 'reasoning') and results.reasoning:
                msg += f"Reasoning: {results.reasoning}"
            return msg
        return "Scenario failed"

