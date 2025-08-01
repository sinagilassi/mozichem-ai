# import libs
from typing import Optional
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


class ChatMessage(BaseModel):
    """
    Model for chat messages, which can be either user or assistant messages.
    """
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the chat message")
    thread_id: Optional[str] = Field(
        None, description="Identifier for the chat thread"
    )
