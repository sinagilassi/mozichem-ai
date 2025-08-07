# import libs
import asyncio
import os
import logging
from mozichem_ai.agents import create_agent
from mozichem_ai.memory import generate_thread
from langchain_core.runnables import RunnableConfig
# python dot env
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

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

# empty mcp source
mcp_source = None

# NOTE: agent prompt
agent_prompt = """You are a helpful assistant that can perform various tasks using tools provided by the EOS Models and Flash Calculations MCP servers.
You can use tools to perform calculations, retrieve data, and assist with various tasks.
Based on the results from the tools, you will provide a final answer to the user.
"""

# NOTE: config
config, thread_id = generate_thread()

# SECTION: run agent


async def run_agent():
    console = Console()
    try:
        # NOTE: create agent
        agent = await create_agent(
            model_provider=model_provider,
            model_name=model_name,
            agent_name="TestAgent",
            agent_prompt=agent_prompt,
            mcp_source=mcp_source,
            memory_mode=True
        )

        # Chat loop
        while True:
            console.rule("[bold blue]User Message")
            user_input = input("You: ")
            if user_input.lower() == "quit":
                console.print(
                    "[bold red]Exiting chat. Goodbye!",
                    style="bold red"
                )
                break

            agent_response = await agent.ainvoke(
                {"messages": user_input},
                config=RunnableConfig(
                    configurable={
                        "thread_id": thread_id
                    }
                )
            )

            console.print(
                Panel(
                    agent_response['messages'][-1].content,
                    title="Agent Response",
                    style="white"
                )
            )
    except Exception as e:
        logger.error(f"Error running agent: {e}")

if __name__ == "__main__":
    asyncio.run(run_agent())
