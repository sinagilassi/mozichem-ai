# import libs
import logging
import time
from typing import (
    Dict,
    Union,
    List,
    Optional
)
from fastapi import (
    FastAPI,
    HTTPException,
    Response
)
from pathlib import Path
from langchain_core.runnables import RunnableConfig
# locals
from .ai_api import MoziChemAIAPI
from ..agents import create_agent
from ..models import (
    ChatMessage,
    AgentConfig,
    LlmConfig,
    ApiConfigSummary,
    OverallSettings,
    AppInfo,
    AgentDetails,
    LlmDetails
)
from ..memory import generate_thread

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
    mcp_source: Optional[
        Union[
        Dict[str, Dict[str, str]],
        Dict[str, Dict[str, str | List[str]]],
        str,
        Path
        ]
    ] = None,
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
    mcp_source : Dict[str, Dict[str, str]] | Dict[str, Dict[str, str | List[str]]], | str | Path, optional
        A dictionary containing the MCP configurations or a path to a YAML file containing the MCP configurations.
    memory_mode : bool, optional
        Whether to enable memory mode for the agent, by default False.
    kwargs : dict
        Additional keyword arguments for future extensions.
        - temperature: float, optional
            The temperature for the LLM, by default 0.0.
        - max_tokens: int, optional
            The maximum number of tokens for the LLM, by default 2048.
        - cors_origins: List[str], optional
            A list of allowed CORS origins. If None, defaults to allowing all origins.
        - name: str, optional
            The name of the API, by default "MoziChem AI API".
        - version: str, optional
            The version of the API, by default "No version set".
        - description: str, optional
            A description of the API, by default "No description set".

    Returns
    -------
    FastAPI
        The FastAPI application instance.
    """
    # NOTE: inputs
    cors_origins = kwargs.get('cors_origins', None)
    name = kwargs.get('name', None)
    version = kwargs.get('version', None)
    description = kwargs.get('description', None)

    # SECTION: Initialize the MoziChem AI API
    MoziChemAIAPI_ = MoziChemAIAPI(
        cors_origins=cors_origins,
        name=name,
        version=version,
        description=description
    )

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
        return Response(
            content='{"message": "MoziChem AI API is running"}',
            media_type="application/json",
            status_code=200
        )

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

            # update the initial arguments
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
                'temperature',
                DEFAULT_TEMPERATURE
            )
            app.state.max_tokens = kwargs.get(
                'max_tokens',
                DEFAULT_MAX_TOKENS
            )

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

    @app.post("/chat", response_model=ChatMessage)
    async def user_agent_chat(
        user_message: ChatMessage
    ):
        """
        Handle user-agent chat interaction.

        Parameters
        ----------
        user_message : ChatMessage
            The message from the user to the agent.

        Returns
        -------
        ChatMessage
            The response from the agent to the user.
        """
        # SECTION: Extract the thread_id from the user message
        thread_id = user_message.thread_id
        user_content = user_message.content

        # NOTE: Generate a new thread if thread_id is not provided
        if not thread_id:
            _, new_thread_id = generate_thread()
            thread_id = new_thread_id
            user_message.thread_id = new_thread_id

        try:
            # SECTION: Ensure the agent is created
            agent = getattr(app.state, "agent", None)
            if agent is None:
                logger.error("MoziChem agent is not created yet.")
                return ChatMessage(
                    role="assistant",
                    content="MoziChem agent is not created yet.",
                    thread_id=thread_id,
                    response_time=None
                )

            # NOTE: Measure computation time
            start_time = time.time()

            # NOTE: Invoke the agent with the user message
            response = await agent.ainvoke(
                {
                    "messages": user_content
                },
                config=RunnableConfig(
                    configurable={
                        "thread_id": thread_id,
                    }
                )
            )

            # NOTE: Measure end time and calculate response time
            end_time = time.time()
            response_time = end_time - start_time

            # SECTION: Check response and return the last message
            # last message is the agent's response
            if response and isinstance(response, dict):
                messages = response.get("messages")
                if messages and isinstance(messages, list):
                    response_message = messages[-1]
                    # NOTE: main response
                    return ChatMessage(
                        role="assistant",
                        content=getattr(response_message,
                                        "content", str(response_message)),
                        thread_id=thread_id,
                        response_time=response_time
                    )
                else:
                    logger.error("Agent did not return any messages.")
                    return ChatMessage(
                        role="assistant",
                        content="Agent did not return any messages.",
                        thread_id=thread_id,
                        response_time=response_time
                    )
            else:
                logger.error("Agent response is not a valid dictionary.")
                return ChatMessage(
                    role="assistant",
                    content="Agent response is not a valid dictionary.",
                    thread_id=thread_id,
                    response_time=response_time
                )
        except Exception as e:
            logger.error(f"Error in user_agent_chat: {e}")
            return ChatMessage(
                role="assistant",
                content=f"Failed to process user message: {e}",
                thread_id=thread_id,
                response_time=None
            )

    # SECTION: Return the FastAPI application instance
    @app.get("/app-info", response_model=ApiConfigSummary)
    async def get_app_info():
        """
        Return app info, agent details, llm details, and overall settings as an ApiConfigSummary model.
        """
        try:
            # NOTE: Get the agent details
            agent_obj = getattr(app.state, "agent", None)

            # NOTE: app info
            app_info = AppInfo(
                name=MoziChemAIAPI_.name,
                version=MoziChemAIAPI_.version,
                description=MoziChemAIAPI_.description,
            )

            # NOTE: Agent details
            agent_details = AgentDetails(
                exists=agent_obj is not None,
                model_name=model_name,
                agent_name=agent_name,
                agent_prompt=agent_prompt,
                mcp_source=mcp_source,
                memory_mode=memory_mode
            )

            # NOTE: LLM details
            llm_details = LlmDetails(
                temperature=getattr(
                    app.state,
                    "temperature",
                    DEFAULT_TEMPERATURE
                ),
                max_tokens=getattr(
                    app.state,
                    "max_tokens",
                    DEFAULT_MAX_TOKENS
                )
            )

            # NOTE: Overall settings
            overall_settings = OverallSettings(
                cors_origins=MoziChemAIAPI_.cors_origins
            )

            # SECTION: Return the ApiConfigSummary model
            return ApiConfigSummary(
                app=app_info,
                agent=agent_details,
                llm=llm_details,
                settings=overall_settings
            )
        except Exception as e:
            logger.error(f"Error in get_app_info: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve app info: {e}"
            )
    return app
