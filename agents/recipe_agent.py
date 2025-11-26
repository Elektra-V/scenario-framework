"""
Recipe Agent with support for both OpenAI and custom gateway.
"""
import os
from base64 import b64encode
from typing import Optional
import scenario
from openai import AsyncOpenAI


# ============================================================================
# CUSTOM GATEWAY CLIENT
# ============================================================================
# Implementation for OpenAI-compatible gateway with Basic Auth
class CustomGatewayClient:
    """
    Client for OpenAI-compatible gateway with Basic Authentication.
    Based on your gateway documentation.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize your gateway client.
        
        Args:
            api_key: Your gateway API key (can be "xxxx" as placeholder)
            base_url: Your gateway base URL (e.g., "https://genai.iais.fraunhofer.de/api/v2")
            username: Gateway username for Basic Auth
            password: Gateway password for Basic Auth
        """
        self.api_key = api_key or "xxxx"
        self.base_url = base_url
        self.username = username
        self.password = password
        
        # Build Basic Auth header
        if username and password:
            token_string = f"{username}:{password}"
            token_bytes = b64encode(token_string.encode())
            auth_header = f"Basic {token_bytes.decode()}"
        else:
            auth_header = None
        
        # Initialize OpenAI client with gateway config
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_headers={"Authorization": auth_header} if auth_header else None,
        )
    
    async def chat_completion(
        self,
        model: str,
        messages: list[dict],
        temperature: float = 0.7,
        extra_headers: Optional[dict] = None,
        extra_body: Optional[dict] = None,
    ) -> dict:
        """
        Call your gateway's chat completion endpoint.
        
        Args:
            model: Model identifier (e.g., "Llama-3-SauerkrautLM")
            messages: List of message dicts with "role" and "content"
            temperature: Sampling temperature
            extra_headers: Optional extra headers (e.g., {"X-Request-ID": "..."})
            extra_body: Optional extra body params (e.g., {"guided_choice": [...]})
            
        Returns:
            OpenAI-compatible response object
        """
        # Convert messages to OpenAI format if needed
        # (messages should already be in correct format)
        
        # Call chat completions endpoint
        response = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        
        # Return the response (it's already OpenAI-compatible)
        return response


# ============================================================================
# RECIPE AGENT ADAPTERS
# ============================================================================

class RecipeAgent(scenario.AgentAdapter):
    """
    Recipe agent that provides vegetarian recipes.
    Can use either OpenAI or custom gateway.
    """
    
    SYSTEM_PROMPT = """You are a vegetarian recipe agent.
Given the user request, ask AT MOST ONE follow-up question,
then provide a complete vegetarian recipe with:
- A list of ingredients
- Step-by-step cooking instructions
Keep your responses concise and focused."""

    def __init__(
        self,
        use_custom_gateway: bool = False,
        model: str = "gpt-4o-mini",
        custom_gateway_config: Optional[dict] = None,
    ):
        """
        Initialize the recipe agent.
        
        Args:
            use_custom_gateway: If True, use custom gateway; else use OpenAI
            model: Model identifier (works for both OpenAI and gateway)
            custom_gateway_config: Config dict for custom gateway
                Example: {"api_key": "...", "base_url": "..."}
        """
        self.use_custom_gateway = use_custom_gateway
        self.model = model
        
        if use_custom_gateway:
            # Initialize custom gateway client
            config = custom_gateway_config or {}
            self.gateway_client = CustomGatewayClient(
                api_key=config.get("api_key"),
                base_url=config.get("base_url"),
                username=config.get("username"),
                password=config.get("password"),
            )
        else:
            # Initialize OpenAI client
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.openai_client = AsyncOpenAI(api_key=api_key)

    async def call(self, input: scenario.AgentInput) -> scenario.AgentReturnTypes:
        """
        Process user messages and return agent response.
        This is the interface Scenario expects.
        """
        # Build messages with system prompt
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            *input.messages,
        ]
        
        if self.use_custom_gateway:
            # Use custom gateway
            response = await self.gateway_client.chat_completion(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            # Response is already OpenAI-compatible ChatCompletion object
            return response.choices[0].message
        else:
            # Use OpenAI
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            return response.choices[0].message


# ============================================================================
# FACTORY FUNCTIONS FOR EASY USAGE
# ============================================================================

def create_openai_agent(model: str = "gpt-4o-mini") -> RecipeAgent:
    """Create agent using OpenAI (for local testing)."""
    return RecipeAgent(use_custom_gateway=False, model=model)


def create_custom_gateway_agent(
    model: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> RecipeAgent:
    """
    Create agent using custom gateway (for company environment).
    
    Args:
        model: Model identifier from your gateway (e.g., "Llama-3-SauerkrautLM")
        api_key: Gateway API key (or use env var, can be "xxxx" as placeholder)
        base_url: Gateway base URL (or use env var)
        username: Gateway username for Basic Auth (or use env var)
        password: Gateway password for Basic Auth (or use env var)
    """
    return RecipeAgent(
        use_custom_gateway=True,
        model=model,
        custom_gateway_config={
            "api_key": api_key or os.getenv("CUSTOM_GATEWAY_API_KEY", "xxxx"),
            "base_url": base_url or os.getenv("CUSTOM_GATEWAY_BASE_URL"),
            "username": username or os.getenv("GENAI_USERNAME"),
            "password": password or os.getenv("GENAI_PASSWORD"),
        },
    )

