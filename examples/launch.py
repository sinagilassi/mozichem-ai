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

# SECTION: inputs
# NOTE: model provider
model_provider = "openai"
# NOTE: model name
model_name = "gpt-4o-mini"

# NOTE: mcp source
mcp_source = {
    "eos-models-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8000/eos-models-mcp/mcp/"
    },
    "flash-calculations-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8000/flash-calculations-mcp/mcp/"
    },
    "thermodynamic-properties-mcp": {
        "transport": "streamable_http",
        "url": "http://127.0.0.1:8000/thermodynamic-properties-mcp/mcp/"
    }
}

mcp_source = None

# NOTE: agent prompt
agent_prompt = """You are a helpful assistant that can perform various tasks using tools provided by the EOS Models and Flash Calculations MCP servers, as well as basic arithmetic operations.
You can use tools to perform calculations, retrieve data, and assist with various tasks.
Based on the results from the tools, you will provide a final answer to the user.
"""

# SECTION: Run the FastAPI application
if __name__ == "__main__":
    mozichem_chat(
        model_provider=model_provider,
        model_name=model_name,
        agent_name="MoziChemAgent",
        agent_prompt=agent_prompt,
        mcp_source=mcp_source,
        memory_mode=True
    )
