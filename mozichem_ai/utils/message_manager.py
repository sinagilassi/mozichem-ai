# import libs
import logging
from fastapi import HTTPException
from typing import Union
from langchain_core.messages import (
    ToolMessage, AIMessage, HumanMessage, SystemMessage
)
# local
from ..models import AgentMessage

# NOTE: logger
logger = logging.getLogger(__name__)


def agent_message_analyzer(
        message: Union[
            ToolMessage,
            AIMessage,
            HumanMessage,
            SystemMessage
        ]) -> AgentMessage:
    """
    Analyzes a list of messages and returns a summary of the content.

    Parameters
    ----------
    message : Union[ToolMessage, AIMessage, HumanMessage, SystemMessage]
        A message object from the LangChain library, which can be of type ToolMessage, AIMessage,
        HumanMessage, or SystemMessage.
    """
    try:
        # SECTION: validate message type
        if not isinstance(
            message,
            (ToolMessage, AIMessage, HumanMessage, SystemMessage)
        ):
            logger.error(f"Invalid message type: {type(message)}")

        # SECTION: analyze message content
        # NOTE: iterate through messages
        if isinstance(message, ToolMessage):
            # tool message
            return AgentMessage(
                type="tool",
                content=message.content,
                tool_calls=None,
                name=message.name if hasattr(message, 'name') else None,
                tool_call_id=message.tool_call_id if hasattr(
                    message, 'tool_call_id') else None
            )
        elif isinstance(message, AIMessage):
            # tool calls
            return AgentMessage(
                type="ai",
                content=message.content,
                tool_calls=message.tool_calls if hasattr(
                    message, 'tool_calls') else None,
                name=message.name if hasattr(message, 'name') else None,
                tool_call_id=None
            )

        elif isinstance(message, HumanMessage):
            # human message
            return AgentMessage(
                type="user",
                content=message.content,
                tool_calls=None,
                name=message.name if hasattr(message, 'name') else None,
                tool_call_id=None
            )

        elif isinstance(message, SystemMessage):
            # system message
            return AgentMessage(
                type="system",
                content=message.content,
                tool_calls=None,
                name=message.name if hasattr(message, 'name') else None,
                tool_call_id=None
            )
        else:
            return AgentMessage(
                type="unknown",
                content=message.content if hasattr(message, 'content') else "",
                tool_calls=None,
                name=None,
                tool_call_id=None
            )

    except Exception as e:
        logger.error(f"Error analyzing messages: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to analyze messages") from e
