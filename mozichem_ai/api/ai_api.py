# import libs
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langgraph.graph.state import CompiledStateGraph
# local imports
from ..agents import create_agent

# NOTE: logger
logger = logging.getLogger(__name__)


class MoziChemAIAPI:
    def __init__(
        self
    ):
        '''
        This initializes the FastAPI application and sets up the necessary middleware.
        It also prepares the MoziChem agent for handling requests.
        '''
        # SECTION: Initialize FastAPI app and agent
        self.app = FastAPI()

        # SECTION: Setup the API middleware
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
