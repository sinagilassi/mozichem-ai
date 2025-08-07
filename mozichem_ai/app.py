# import libs
import logging
import os
import uvicorn
import asyncio
from typing import (
    Dict,
    List,
    Union,
    Optional
)
from pathlib import Path
import mimetypes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import webbrowser
# local
from .api import create_api

# NOTE: logger
logger = logging.getLogger(__name__)


def mozichem_chat(
    model_provider: str,
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
    host: str = "127.0.0.1",
    port: int = 8000,
    log_level: str = "info",
        **kwargs):
    """
    Create UI for MoziChem Chat.

    Parameters
    ----------
    model_provider : str
        The provider of the LLM (e.g., "openai", "google", "anthropic").
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
    host : str, optional
        The host address for the FastAPI application, by default "127.0.0.1".
    port : int, optional
        The port for the FastAPI application, by default 8000.
    log_level : str, optional
        The logging level for the FastAPI application, by default "info".
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
    None
        This function does not return anything. It opens web UI for MoziChem Chat.
    """
    try:
        # SECTION: Create the FastAPI application instance
        app_instance: FastAPI = asyncio.run(create_api(
            model_provider=model_provider,
            model_name=model_name,
            agent_name=agent_name,
            agent_prompt=agent_prompt,
            mcp_source=mcp_source,
            memory_mode=memory_mode,
            **kwargs
        )
        )

        # log
        logger.info(
            f"FastAPI application created successfully with model: {model_name}, agent: {agent_name}")

        # SECTION: Set up MIME types for static files
        mimetypes.add_type("text/css", ".css")
        mimetypes.add_type("application/javascript", ".js")
        mimetypes.add_type("image/svg+xml", ".svg")
        mimetypes.add_type("image/png", ".png")
        mimetypes.add_type("image/jpeg", ".jpg")
        mimetypes.add_type("image/gif", ".gif")
        mimetypes.add_type("application/json", ".json")
        mimetypes.add_type("font/woff", ".woff")
        mimetypes.add_type("font/woff2", ".woff2")
        mimetypes.add_type("application/font-ttf", ".ttf")
        mimetypes.add_type("application/vnd.ms-fontobject", ".eot")

        # SECTION: Mount Angular static files
        # path to the Angular dist directory
        angular_dist_path = os.path.join(
            os.path.dirname(__file__),
            'ui',
            'browser'
        )

        # mount static files
        app_instance.mount(
            "/",
            StaticFiles(directory=angular_dist_path, html=True),
            name="static"
        )

        # SECTION: frontend and backend settings
        # NOTE: Open web UI for MoziChem Chat
        webbrowser.open(f"http://{host}:{port}")
        # NOTE: Run the FastAPI application
        uvicorn.run(
            app_instance,
            host=host,
            port=port,
            log_level=log_level
        )
        # log
        logger.info(f"FastAPI application running at http://{host}:{port}")
    except Exception as e:
        logger.error(f"Error creating FastAPI application: {e}")
        raise e
