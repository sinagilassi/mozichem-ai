# import libs
import logging
from typing import (
    Dict,
    Union,
    List
)
from fastapi import (
    FastAPI,
    HTTPException,
    Response
)
from pathlib import Path
# locals
from .ai_api import MoziChemAIAPI
from ..agents import create_agent
from ..models import (
    UserMessage,
    AgentMessage,
    AgentConfig,
    LlmConfig
)

# NOTE: logger
logger = logging.getLogger(__name__)

# NOTE: constants
# temperature and max_tokens for the LLM
DEFAULT_TEMPERATURE = 0.0
DEFAULT_MAX_TOKENS = 2048


async def create_api(
    model_name: str,
    agent_name: str,
    agent_prompt: str,
    mcp_source: Union[
        Dict[str, Dict[str, str]],
        Dict[str, Dict[str, str | List[str]]],
        str,
        Path
    ],
    memory_mode: bool = False,
    **kwargs
) -> FastAPI:
    """
    Create and return a FastAPI application instance with the MoziChem AI API.

    Parameters
    ----------
    model_name : str
        The name of the model to be used for the agent.
    agent_name : str
        The name of the agent.
    agent_prompt : str
        The prompt to be used for the agent.
    mcp_source : Dict[str, Dict[str, str]] | Dict[str, Dict[str, str | List[str]]], | str | Path
        A dictionary containing the MCP configurations or a path to a YAML file containing the MCP configurations.
    memory_mode : bool, optional
        Whether to enable memory mode for the agent, by default False.
    kwargs : dict
        Additional keyword arguments for future extensions.

    Returns
    -------
    FastAPI
        The FastAPI application instance.
    """
    # SECTION: create agent
    # Use app.state for shared agent instance

    # SECTION: Initialize the MoziChem AI API
    MoziChemAIAPI_ = MoziChemAIAPI()

    # NOTE: create fastapi app instance
    app = MoziChemAIAPI_.app

    # SECTION: Register the API routes

    async def agent_initialization():
        """
        Initialize the agent with the provided parameters.
        """
        try:
            app.state.agent = await create_agent(
                model_name=model_name,
                agent_name=agent_name,
                agent_prompt=agent_prompt,
                mcp_source=mcp_source,
                memory_mode=memory_mode,
                **kwargs
            )
            return Response(
                content='{"message": "Agent initialized successfully"}',
                media_type="application/json",
                status_code=200
            )
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize agent: {e}"
            )

    @app.get("/")
    async def root():
        """
        Root endpoint to check if the API is running.
        """
        return Response(content='{"message": "MoziChem AI API is running"}', media_type="application/json", status_code=200)

    @app.get("/agent-initialization")
    async def initialize_agent():
        """
        Endpoint to initialize the agent with the provided parameters.
        """
        return await agent_initialization()

    @app.post("/agent-config")
    async def set_agent_config(
        agent_config: AgentConfig
    ):
        """
        Config the agent with the necessary parameters.
        """
        try:
            # SECTION: extract parameters from the agent_config
            model_name_ = agent_config.model_name
            agent_name_ = agent_config.agent_name
            agent_prompt_ = agent_config.agent_prompt
            mcp_source_ = agent_config.mcp_source
            memory_mode_ = agent_config.memory_mode

            # SECTION: validate the agent configuration
            # NOTE: update the initial arguments
            nonlocal model_name, agent_name, agent_prompt, mcp_source, memory_mode
            if model_name_ is not None:
                model_name = model_name_
            if agent_name_ is not None:
                agent_name = agent_name_
            if agent_prompt_ is not None:
                agent_prompt = agent_prompt_
            if mcp_source_ is not None:
                mcp_source = mcp_source_
            if memory_mode_ is not None:
                memory_mode = memory_mode_

            # SECTION: llm configuration
            app.state.temperature = kwargs.get(
                'temperature', DEFAULT_TEMPERATURE)
            app.state.max_tokens = kwargs.get('max_tokens', DEFAULT_MAX_TOKENS)

            # update kwargs with the new values
            kwargs['temperature'] = app.state.temperature
            kwargs['max_tokens'] = app.state.max_tokens

            # NOTE: create or update the agent in app.state
            app.state.agent = await create_agent(
                model_name=model_name,
                agent_name=agent_name,
                agent_prompt=agent_prompt,
                mcp_source=mcp_source,
                memory_mode=memory_mode,
                **kwargs
            )
            return Response(
                content='{"message": "Agent configured successfully"}',
                media_type="application/json",
                status_code=200
            )
        except Exception as e:
            logger.error(f"Error configuring agent: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to configure agent: {e}")

    @app.post("/llm-config")
    async def set_llm_config(
        llm_config: LlmConfig
    ):
        """
        Config the LLM with the necessary parameters.
        """
        try:
            # SECTION: extract parameters from the llm_config
            model_name_ = llm_config.model_name
            temperature_ = llm_config.temperature
            max_tokens_ = llm_config.max_tokens

            # NOTE: update the agent's LLM configuration
            if model_name_ is not None:
                model_name = model_name_
            if temperature_ is not None:
                # update the kwargs for temperature
                kwargs['temperature'] = temperature_
                # app sate
                app.state.temperature = temperature_
            if max_tokens_ is not None:
                # update the kwargs for max_tokens
                kwargs['max_tokens'] = max_tokens_
                # app state
                app.state.max_tokens = max_tokens_

            # SECTION: reinitialize the agent with the new LLM configuration
            app.state.agent = await create_agent(
                model_name=model_name,
                agent_name=agent_name,
                agent_prompt=agent_prompt,
                mcp_source=mcp_source,
                memory_mode=memory_mode,
                **kwargs
            )

            # NOTE: return success message
            logger.info("LLM configured successfully")
            return Response(
                content='{"message": "LLM configured successfully"}',
                media_type="application/json",
                status_code=200
            )
        except Exception as e:
            logger.error(f"Error configuring LLM: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to configure LLM: {e}")

    @app.post("/chat", response_model=AgentMessage)
    async def user_agent_chat(
        user_message: UserMessage,
    ):
        """
        Handle user-agent chat interaction.

        Parameters
        ----------
        user_message : UserMessage
            The message from the user to the agent.

        Returns
        -------
        List[AgentMessage]
            A list of messages from the agent in response to the user's
            message.
        """
        try:
            # SECTION: Ensure the agent is created
            agent = getattr(app.state, "agent", None)
            if agent is None:
                logger.error("MoziChem agent is not created yet.")
                raise HTTPException(
                    status_code=500, detail="MoziChem agent is not created yet.")

            # NOTE: Process the user message and get the agent's response
            response = await agent.ainvoke(user_message)

            # last message is the agent's response
            if response:
                response = response['messages'][-1]

            return response
        except Exception as e:
            logger.error(f"Error in user_agent_chat: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to process user message: {e}")

    # SECTION: Return the FastAPI application instance
    return app
