# import libs
from typing import Dict, List, Union, Any
from pathlib import Path
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    """
    Model for user messages in the chat.
    """
    role: str = Field("user", description="Role of the message sender")
    content: str = Field(..., description="Content of the user message")


class AssistantMessage(BaseModel):
    """
    Model for assistant messages in the chat.
    """
    role: str = Field("assistant", description="Role of the message sender")
    content: str = Field(..., description="Content of the assistant message")


class AgentMessage(BaseModel):
    """
    Model for agent messages in the chat.
    """
    role: str = Field("agent", description="Role of the message sender")
    content: str = Field(..., description="Content of the agent message")
