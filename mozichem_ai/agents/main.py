# import libs
import logging
from typing import (
    Dict,
    List,
    Union,
    Optional
)
from pathlib import Path
from langgraph.graph.state import CompiledStateGraph
# local
from .mozichem_agent import MoziChemAgent

# NOTE: logger
logger = logging.getLogger(__name__)


async def create_agent(
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
) -> CompiledStateGraph:
    """
    Create and return a langgraph agent with the specified model name.

    Parameters
    ----------
    model_name : str
        The name of the model to be used for the agent.
    agent_name : str
        The name of the agent.
    agent_prompt : str
        The prompt to be used for the agent.
    mcp_source : Dict[str, stdioMCP | streamableHttpMCP] | Path
        A dictionary containing the MCP configurations or a path to a YAML file containing the MCP configurations.
    memory_mode : bool, optional
        Whether to enable memory mode for the agent, by default False.
    kwargs : dict
        Additional keyword arguments for future extensions.

    Returns
    -------
    agent: CompiledStateGraph
        The compiled state graph of the agent.
    """
    try:
        # SECTION: create MoziChemAgent
        MoziChemAgent_ = MoziChemAgent(
            model_name,
            agent_name,
            agent_prompt,
            mcp_source,
            memory_mode,
            **kwargs
        )

        # SECTION: initialize the agent
        agent = await MoziChemAgent_.build_agent()

        return agent
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise RuntimeError(f"Failed to create agent: {e}") from e
