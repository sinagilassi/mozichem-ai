# import libs
import logging
from typing import Dict, Any, Union, List
from pathlib import Path
from fastapi import FastAPI, HTTPException
# locals
from .ai_api import MoziChemAIAPI
from ..agents import create_agent
from ..models import UserMessage, AgentMessage

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
            if MoziChemAIAPI_.agent is None:
                logger.error("MoziChem agent is not created yet.")
                raise HTTPException(
                    status_code=500, detail="MoziChem agent is not created yet.")

            # Process the user message and get the agent's response
            response = await \
                MoziChemAIAPI_.agent.ainvoke(user_message)

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
