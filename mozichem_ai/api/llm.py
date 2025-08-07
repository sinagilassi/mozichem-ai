# import libs
import logging
from fastapi import HTTPException, APIRouter
# local imports
from ..llms import LlmManager
from ..config import llm_providers


# NOTE: logger
logger = logging.getLogger(__name__)

# SECTION: api router
llm_router = APIRouter()

# SECTION: routes


@llm_router.get("/llm/ping", response_model=bool)
async def check_llm(
    model_provider: str,
    model_name: str,
):
    """
    Initialize the LLM with the given parameters.

    Parameters
    ----------
    model_provider : str
        The provider of the LLM (e.g., "openai", "google", "anthropic").
    model_name : str
        The name of the LLM model to initialize (e.g., "gpt-3.5-turbo", "gemini-1.5-pro").
    """
    try:
        # SECTION: validate inputs
        if not model_provider or not model_name:
            raise HTTPException(
                status_code=400, detail="Model provider and name must be provided.")

        # NOTE: check if model provider is supported
        if model_provider not in llm_providers:
            raise HTTPException(
                status_code=400, detail=f"Unsupported model provider: {model_provider}. Supported providers are: {', '.join(llm_providers)}.")

        # SECTION: init llm manager
        llm_manager = LlmManager(
            model_provider=model_provider,
            model_name=model_name
        )

        # SECTION: ping the model
        response = llm_manager.ping()

        return response
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        raise HTTPException(status_code=500, detail=str(e))
