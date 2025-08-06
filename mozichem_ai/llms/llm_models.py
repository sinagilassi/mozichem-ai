# import libs
import logging
from langchain.chat_models import init_chat_model
from typing import (
    Dict,
    Union,
    List,
    Any,
    Literal
)
# local

# NOTE: logger
logger = logging.getLogger(__name__)


def initialize_model(
    model_provider: Literal["openai", "google", "anthropic"],
    model_name: str,
    **kwargs
) -> Any:
    """
    Initialize and return a chat model based on the specified model name.

    Parameters
    ----------
    model_company : str
        The company or provider of the model (e.g., "openai", "google").
    model_name : str
        The name of the model to be initialized.
    kwargs : dict
        Additional keyword arguments for future extensions.

    Returns
    -------
    model: Any
        The initialized chat model.
    """
    try:
        # SECTION: validate model provider
        valid_providers = ["openai", "google", "anthropic"]
        if model_provider not in valid_providers:
            raise ValueError(
                f"Invalid model provider: {model_provider}. Supported providers are: {valid_providers}")

        # SECTION: initialize model
        model = init_chat_model(
            model_name=model_name,
            model_provider=model_provider,
            **kwargs
        )
        return model
    except Exception as e:
        logger.error(
            f"Error initializing model {model_name} from {model_provider}: {e}")
        raise
