# import libs
import os
import logging
# python dot env
from dotenv import load_dotenv
# local
from mozichem_ai import mozichem_chat

# NOTE: logger
logger = logging.getLogger(__name__)

# SECTION: load environment variables
load_dotenv()

# langchain
env_val = os.getenv('LANGCHAIN_API_KEY')
if env_val is not None:
    os.environ['LANGCHAIN_API_KEY'] = env_val
env_val = os.getenv('LANGCHAIN_TRACING_V2')
if env_val is not None:
    os.environ['LANGCHAIN_TRACING_V2'] = env_val

# open ai
env_val = os.getenv('OPENAI_API_KEY')
if env_val is not None:
    os.environ['OPENAI_API_KEY'] = env_val

# tavily
env_val = os.getenv('TAVILY_API_KEY')
if env_val is not None:
    os.environ['TAVILY_API_KEY'] = env_val

# SECTION: inputs
# NOTE: model provider
model_provider = "openai"
# NOTE: model name
model_name = "gpt-4o-mini"

# NOTE: mcp source
mcp_source = {
    "eos-models-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8001/eos-models-mcp/mcp/",
        "env": {}
    },
    "flash-calculations-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8001/flash-calculations-mcp/mcp/",
        "env": {}
    },
    "thermodynamic-properties-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8001/thermodynamic-properties-mcp/mcp/",
        "env": {}
    }
}

# mcp source 2
mcp_source = {
    "tavily-remote": {
        "command": "npx",
        "args": [
            "-y",
            "mcp-remote",
            f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}"
        ],
        "transport": "stdio",
        "env": {}
    }
}

mcp_source = None

# NOTE: agent prompt
agent_prompt = """You are a helpful assistant. You can use MCP server tools and basic arithmetic to solve problems, retrieve data, and perform calculations.
When a user asks a question, select the most appropriate tool or method, explain your reasoning briefly, and provide a clear final answer based on the results.
Always be concise, accurate, and helpful in your responses.
"""

# SECTION: Run the FastAPI application
if __name__ == "__main__":
    mozichem_chat(
        model_provider=model_provider,
        model_name=model_name,
        agent_name="MoziChemAgent",
        agent_prompt=agent_prompt,
        mcp_source=mcp_source,
        memory_mode=True,
        open_browser=True,
    )
