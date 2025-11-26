"""
Script to list available models from OpenAI or custom gateway.
Shows both chat/completion models and embedding models.
"""
import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from base64 import b64encode

# Load environment variables
load_dotenv()

# Configuration
USE_CUSTOM_GATEWAY = os.getenv("USE_CUSTOM_GATEWAY", "false").lower() == "true"
GATEWAY_BASE_URL = os.getenv("CUSTOM_GATEWAY_BASE_URL", "https://genai.iais.fraunhofer.de/api/v2")
GATEWAY_API_KEY = os.getenv("CUSTOM_GATEWAY_API_KEY", "xxxx")
GENAI_USERNAME = os.getenv("GENAI_USERNAME")
GENAI_PASSWORD = os.getenv("GENAI_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


async def create_client():
    """Create OpenAI client for either OpenAI or custom gateway."""
    if USE_CUSTOM_GATEWAY:
        # Build Basic Auth header
        if GENAI_USERNAME and GENAI_PASSWORD:
            token_string = f"{GENAI_USERNAME}:{GENAI_PASSWORD}"
            token_bytes = b64encode(token_string.encode())
            auth_header = f"Basic {token_bytes.decode()}"
        else:
            auth_header = None
        
        return AsyncOpenAI(
            api_key=GATEWAY_API_KEY,
            base_url=GATEWAY_BASE_URL,
            default_headers={"Authorization": auth_header} if auth_header else None,
        )
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment")
        return AsyncOpenAI(api_key=OPENAI_API_KEY)


async def list_chat_models(client):
    """List available chat/completion models."""
    print("\n" + "=" * 60)
    print("CHAT/COMPLETION MODELS")
    print("=" * 60)
    
    try:
        models = await client.models.list()
        if models.data:
            print(f"\nFound {len(models.data)} model(s):\n")
            for model in models.data:
                print(f"  • {model.id}")
                if hasattr(model, 'created') and model.created:
                    print(f"    Created: {model.created}")
                if hasattr(model, 'owned_by') and model.owned_by:
                    print(f"    Owned by: {model.owned_by}")
                print()
        else:
            print("\nNo models found via models.list() endpoint.")
            print("This gateway might not support the models listing endpoint.")
    except Exception as e:
        print(f"\n⚠️  Error listing models: {e}")
        print("\nTrying alternative method: testing known model names...")
        
        # Try some common model names
        test_models = [
            "Llama-3-SauerkrautLM",
            "llama-3-70b",
            "gpt-4o-mini",
            "gpt-4",
            "gpt-3.5-turbo",
        ]
        
        print("\nTesting model availability:")
        for model_name in test_models:
            try:
                # Try a minimal completion to see if model exists
                response = await client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1,
                )
                print(f"  ✅ {model_name} - Available")
            except Exception as err:
                error_msg = str(err).lower()
                if "model" in error_msg and ("not found" in error_msg or "invalid" in error_msg):
                    print(f"  ❌ {model_name} - Not available")
                else:
                    # Other error might mean model exists but request failed
                    print(f"  ⚠️  {model_name} - Might be available (error: {str(err)[:50]}...)")
            except:
                print(f"  ❌ {model_name} - Not available")


async def list_embedding_models(client):
    """List available embedding models."""
    print("\n" + "=" * 60)
    print("EMBEDDING MODELS")
    print("=" * 60)
    
    try:
        # Try to get models and filter for embeddings
        models = await client.models.list()
        embedding_models = []
        
        if models.data:
            # Check each model - some gateways mark embedding models differently
            for model in models.data:
                model_id = model.id.lower()
                # Common patterns for embedding models
                if any(keyword in model_id for keyword in [
                    "embed", "ada-002", "text-embedding", "mpnet", "sentence"
                ]):
                    embedding_models.append(model.id)
        
        if embedding_models:
            print(f"\nFound {len(embedding_models)} embedding model(s):\n")
            for model_id in embedding_models:
                print(f"  • {model_id}")
        else:
            print("\nNo embedding models found via models.list() endpoint.")
            print("Trying alternative method: testing known embedding model names...")
            
            # Try some common embedding model names
            test_models = [
                "all-mpnet-base-v2",  # From your gateway docs
                "text-embedding-ada-002",
                "text-embedding-3-small",
                "text-embedding-3-large",
            ]
            
            print("\nTesting embedding model availability:")
            for model_name in test_models:
                try:
                    response = await client.embeddings.create(
                        model=model_name,
                        input=["test"],
                    )
                    print(f"  ✅ {model_name} - Available")
                    if hasattr(response, 'data') and response.data:
                        dims = len(response.data[0].embedding) if response.data[0].embedding else "unknown"
                        print(f"      Dimensions: {dims}")
                except Exception as err:
                    error_msg = str(err).lower()
                    if "model" in error_msg and ("not found" in error_msg or "invalid" in error_msg):
                        print(f"  ❌ {model_name} - Not available")
                    else:
                        print(f"  ⚠️  {model_name} - Might be available (error: {str(err)[:50]}...)")
                except:
                    print(f"  ❌ {model_name} - Not available")
                    
    except Exception as e:
        print(f"\n⚠️  Error listing embedding models: {e}")
        print("\nTrying direct test with known model from your gateway docs:")
        try:
            response = await client.embeddings.create(
                model="all-mpnet-base-v2",
                input=["test"],
            )
            print("  ✅ all-mpnet-base-v2 - Available")
            if hasattr(response, 'data') and response.data:
                dims = len(response.data[0].embedding) if response.data[0].embedding else "unknown"
                print(f"      Dimensions: {dims}")
        except Exception as err:
            print(f"  ❌ all-mpnet-base-v2 - Error: {err}")


async def test_model_access(client, model_name: str):
    """Test if we can access a specific model."""
    print(f"\nTesting access to model: {model_name}")
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say 'test'"}],
            max_tokens=5,
        )
        print(f"  ✅ Success! Response: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


async def main():
    """Main function to list all models."""
    print("=" * 60)
    print("MODEL LISTING TOOL")
    print("=" * 60)
    
    if USE_CUSTOM_GATEWAY:
        print(f"\n🔧 Using Custom Gateway")
        print(f"   Base URL: {GATEWAY_BASE_URL}")
        if GENAI_USERNAME:
            print(f"   Username: {GENAI_USERNAME}")
        else:
            print(f"   ⚠️  GENAI_USERNAME not set")
    else:
        print(f"\n🔧 Using OpenAI")
        if not OPENAI_API_KEY:
            print("   ⚠️  OPENAI_API_KEY not set")
    
    try:
        client = await create_client()
        
        # List chat/completion models
        await list_chat_models(client)
        
        # List embedding models
        await list_embedding_models(client)
        
        # Optional: Test a specific model if provided
        test_model = os.getenv("TEST_MODEL")
        if test_model:
            print("\n" + "=" * 60)
            print("TESTING SPECIFIC MODEL")
            print("=" * 60)
            await test_model_access(client, test_model)
        
        print("\n" + "=" * 60)
        print("Done!")
        print("=" * 60)
        print("\n💡 Tip: Set TEST_MODEL=<model_name> in .env to test a specific model")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your environment variables are set correctly:")
        if USE_CUSTOM_GATEWAY:
            print("  - CUSTOM_GATEWAY_BASE_URL")
            print("  - GENAI_USERNAME")
            print("  - GENAI_PASSWORD")
        else:
            print("  - OPENAI_API_KEY")


if __name__ == "__main__":
    asyncio.run(main())

