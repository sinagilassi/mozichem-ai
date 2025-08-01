# import libs
import logging
from typing import Dict, Any, Union, List
from pathlib import Path
from fastapi import FastAPI, HTTPException
from langchain_core.runnables import RunnableConfig
# locals
from .ai_api import MoziChemAIAPI
from ..agents import create_agent
from ..models import ChatMessage
from ..memory import generate_thread

# NOTE: logger
logger = logging.getLogger(__name__)


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
    memory_mode: bool = False
) -> FastAPI:
    """
    Create and return a FastAPI application instance with the MoziChem AI API.

    Returns
    -------
    FastAPI
        The FastAPI application instance.
    """
    # SECTION: create agent
    agent = await create_agent(
        model_name=model_name,
        agent_name=agent_name,
        agent_prompt=agent_prompt,
        mcp_source=mcp_source,
        memory_mode=memory_mode
    )

    # SECTION: Initialize the MoziChem AI API
    MoziChemAIAPI_ = MoziChemAIAPI(agent=agent)

    # NOTE: create fastapi app instance
    app = MoziChemAIAPI_.app

    # SECTION: Register the API routes

    @app.get("/")
    async def root():
        """
        Root endpoint to check if the API is running.
        """
        return {"message": "MoziChem AI API is running"}

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
        try:
            # NOTE: get thread id from user message
            thread_id = user_message.thread_id

            # check if thread_id is provided
            if not thread_id:
                # generate a new thread if not provided
                _, thread_id = generate_thread()

            if MoziChemAIAPI_.agent is None:
                logger.error("MoziChem agent is not created yet.")
                raise HTTPException(
                    status_code=500, detail="MoziChem agent is not created yet.")

            # NOTE: user message
            user_input = user_message.content

            # NOTE: Process the user message and get the agent's response
            response = await \
                MoziChemAIAPI_.agent.ainvoke(
                    {"messages": user_input},
                    config=RunnableConfig(
                        configurable={
                            "thread_id": thread_id
                        }
                    )
                )

            # last message is the agent's response
            if response:
                response_message = response['messages'][-1]

            return ChatMessage(
                role="assistant",
                content=response_message.content,
                thread_id=thread_id
            )
        except Exception as e:
            logger.error(f"Error in user_agent_chat: {e}")
            raise HTTPException(
                status_code=500, detail=f"Failed to process user message: {e}")

    # SECTION: Return the FastAPI application instance
    return app
