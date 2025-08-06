# import libs
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, APIRouter
# local imports
from ..llms import initialize_model
