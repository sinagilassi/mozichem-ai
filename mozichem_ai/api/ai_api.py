# import libs
import logging
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Callable
# local imports
from ..agents import create_agent
from ..models import UserMessage, AgentMessage


class MoziChemAIAPI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.app = FastAPI()
        self.router = APIRouter()
        self.mozichem_agent = None
        self._setup_middleware()

    def _setup_middleware(self):
        """Setup middleware for the FastAPI application."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Allow all origins
            allow_credentials=True,
            allow_methods=["*"],  # Allow all methods
            allow_headers=["*"],  # Allow all headers
        )

    async def create_mozichem_agent(
        self,
        model_name: str,
        agent_name: str,
        agent_prompt: str,
        mcp_source: Dict[str, Any],
        memory_mode: bool = False
    ):
        """
        Create a MoziChem agent with the specified parameters.

        Parameters
        ----------
        model_name : str
            The name of the model to be used for the agent.
        agent_name : str
            The name of the agent.
        agent_prompt : str
            The prompt to be used for the agent.
        mcp_source : Dict[str, Any]
            A dictionary containing the MCP configurations.
        memory_mode : bool, optional
            Whether to enable memory mode for the agent, by default False.
        """
        if self.mozichem_agent is None:
            self.mozichem_agent = await create_agent(
                model_name=model_name,
                agent_name=agent_name,
                agent_prompt=agent_prompt,
                mcp_source=mcp_source,
                memory_mode=memory_mode
            )
        return self.mozichem_agent

    async def user_agent_chat(
        self,
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
            if self.mozichem_agent is None:
                raise ValueError("MoziChem agent is not created yet.")

            # Process the user message and get the agent's response
            response = await self.mozichem_agent.ainvoke(user_message)
            return response
        except Exception as e:
            self.logger.error(f"Error in user_agent_chat: {e}")
            raise ValueError(f"Failed to process user message: {e}") from e


# Instantiate the API class
mozichemai_api = MoziChemAIAPI()
app = mozichemai_api.app
