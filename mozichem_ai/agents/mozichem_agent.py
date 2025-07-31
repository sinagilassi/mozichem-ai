# import libs
import logging
from typing import Dict, Optional, Union, List, Any
from pathlib import Path
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
# local
from mozichem_ai.models import stdioMCP, streamableHttpMCP, MCP
from mozichem_ai.agents.mcp_manager import MCPManager

# NOTE: logger
logger = logging.getLogger(__name__)


class MoziChemAgent:
    '''
    MoziChem Agent class for creating and managing agents using langchain and langgraph.
    '''
    # NOTE: attributes
    # mcp lists
    _mcp_list = {}
    # agent prompt
    _agent_prompt = None
    # memory mode
    _memory_mode = False
    # agent name
    _agent_name = None

    def __init__(
        self,
        model_name: str,
        agent_name: str,
        agent_prompt: str,
        mcp_source: Union[
            Dict[str, Dict[str, str]],
            Dict[str, Dict[str, str | List[str]]],
            str,
            Path
        ],
        memory_mode: bool
    ):
        '''
        Initialize the MoziChemAgent with a model name and additional parameters.

        Parameters
        ----------
        model_name : str
            The name of the model to be used for the agent.
        agent_name : str
            The name of the agent.
        agent_prompt : str
            The prompt to be used for the agent.
        mcp_source : Dict[str, Dict[str, str]] | Dict[str, Dict[str, str | List[str]]]
            A dictionary containing the MCP configurations.
        memory_mode : bool
            Whether to enable memory mode for the agent.
        '''
        # NOTE: set attributes
        self._model_name = model_name
        self._agent_name = agent_name
        self._agent_prompt = agent_prompt
        self.mcp_source = mcp_source
        self._memory_mode = memory_mode

        # SECTION: initialize LLM
        self.init_llm()

        # SECTION: adapt MCP
        self.adapt_mcp()

        # SECTION: create client
        self.create_client()

    def init_llm(self):
        '''
        This method sets up the language model for the agent using the model name provided during initialization.
        It uses the `init_chat_model` function from langchain to create the model instance.
        '''
        try:
            self.llm = init_chat_model(self._model_name)
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise RuntimeError(f"Failed to initialize LLM: {e}") from e

    def adapt_mcp(self):
        '''
        This method adapts the MCP configurations based on the provided mcp_source.
        '''
        try:
            # NOTE: init MCPManager
            MCPManager_ = MCPManager(self.mcp_source)

            # NOTE: mcp config
            mcp_ = MCPManager_.config_mcp()

            # SECTION: convert to MCP dict for MultiServerMCPClient
            if isinstance(mcp_, dict):
                # stdio mcp dict
                self.mcp_stdio_dict = {
                    name: stdioMCP(**config).model_dump()
                    for name, config in mcp_.items()
                    if isinstance(config, dict) and config.get('transport') == 'stdio'
                }

                # streamable http mcp dict
                self.mcp_streamable_http_dict = {
                    name: streamableHttpMCP(**config).model_dump()
                    for name, config in mcp_.items()
                    if isinstance(config, dict) and config.get('transport') == 'streamable_http'
                }
        except Exception as e:
            logger.error(f"Failed to adapt MCP: {e}")
            raise RuntimeError(f"Failed to adapt MCP: {e}") from e

    def create_client(self):
        '''
        Create and return a MultiServerMCPClient instance with the MCP configurations.
        '''
        try:
            # section: mcp feed
            mcp_feed: Dict[str, Any] = {
                **self.mcp_stdio_dict,
                **self.mcp_streamable_http_dict
            }

            # SECTION: create MCP client
            self.client = MultiServerMCPClient(
                mcp_feed
            )
        except Exception as e:
            logger.error(f"Failed to create MCP client: {e}")
            raise RuntimeError(f"Failed to create MCP client: {e}") from e

    async def build_agent(self):
        '''
        build and return a langgraph agent using the initialized LLM and MCP client.
        '''
        try:
            # SECTION: client and tools
            client = self.client
            # get tools
            tools = await client.get_tools()

            # SECTION: memory saver
            if self._memory_mode:
                memory = MemorySaver()
            else:
                memory = None

            # SECTION: create agent
            agent = create_react_agent(
                model=self.llm,
                tools=tools,
                prompt=self._agent_prompt,
                checkpointer=memory
            )

            # return agent
            return agent
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise RuntimeError(f"Failed to initialize agent: {e}") from e
