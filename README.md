# MoziChem-AI

![MoziChem-AI Logo](https://drive.google.com/uc?export=view&id=1WKN5vQCt8TeIltix0_oHtrME6bV5X6EK)

[![PyPI Downloads](https://static.pepy.tech/badge/mozichem-ai/month)](https://pepy.tech/projects/mozichem-ai)
![PyPI Version](https://img.shields.io/pypi/v/mozichem-ai)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/mozichem-ai.svg)
![License](https://img.shields.io/pypi/l/mozichem-ai)
[![MCP](https://img.shields.io/badge/Model_Context_Protocol-Compatible-orange)](https://modelcontextprotocol.io)

MoziChem-AI is a modern Python-powered UI for interacting with LLM agents via [LangGraph](https://github.com/langchain-ai/langgraph).
It lets you easily configure LLM model parameters, connect to multiple Model Context Protocol (MCP) tools, and track agent reasoning in real time.

![MoziChem-AI UI](https://drive.google.com/uc?export=view&id=1TUWYEAoyqYlBKlN1LSt6O5dcB3OoMYYT)

  Dynamic MCP Tool Management — MoziChem-AI lets you attach or detach any number of MCP tools at runtime. Once changes are made, you can restart the LangGraph agent with the updated toolset, enabling instant reconfiguration without modifying the underlying code.

![MoziChem-AI MCP](https://drive.google.com/uc?export=view&id=1_8ZV3loqA-H2BFH8arpp7hExiYtxxVkq)

---

## 🏗️ Architecture

**Backend:** FastAPI

- Manages the LLM agent
- Integrates MCP tools
- Streams responses and agent steps

**Frontend:** Angular

- Fast, reactive UI
- Configure, interact, and track the agent

---

## ⚡ Key Features

### Interactive LLM Configuration

- Choose model provider (OpenAI, Anthropic, Gemini, etc.)
- Select model name
- Adjust temperature, max tokens, and more

### LangGraph Agent Integration

- Core agent defined with LangGraph
- Supports multi-MCP connections (attach multiple external tool APIs)
- Automatic reasoning and tool chaining

### Multi-MCP Tool Support

- Works with MoziChem-Hub or any MCP-compatible server
- Tools range from chemistry models to general automation
- Call MCPs independently or in combination during conversations

### Response Tracking & Streaming

- View agent steps in real time
- Monitor MCP tool calls, inputs, and outputs
- Ideal for debugging, transparency, and validation

---


## 📦 Dependencies

The main dependencies required for MoziChem-AI are:

```
fastapi[standard]>=0.115.14
langchain>=0.3.27
langchain-anthropic>=0.3.18
langchain-google-genai>=2.1.8
langchain-openai>=0.3.27
langchain-mcp-adapters>=0.1.8
langgraph>=0.6.3
pydantic>=2.11.7
pydantic-settings>=2.10.1
python-dotenv>=1.1.1
rich>=14.0.0
websockets>=15.0.1
```

These packages are automatically installed when you run:

```bash
pip install mozichem-ai
```

---


## 🚀 Get Started

1. Install the local agent:

  ```bash
  pip install mozichem-ai
  ```

---

## 🖥️ Launch the App

To start the MoziChem-AI agent with browser UI and MCP tool support, use the provided `launch.py` script:

1.**Set up your environment variables**

- Create a `.env` file in the project root and add your API keys (e.g., `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `TAVILY_API_KEY`).

2.**Run the launch script**

- From the `examples` directory, execute:

```bash
uv run launch.py
```

This will:

- Load your environment variables
- Configure the agent and MCP sources
- Start the FastAPI backend
- Automatically open the browser UI for interaction

You can customize the agent prompt, model provider, and MCP sources by editing `examples/launch.py`.

---

## ⚙️ `launch.py` Method Details

The `launch.py` script uses the `mozichem_chat` method to start the agent and UI. Here are the main arguments and how to set them:

### Arguments for `mozichem_chat`

**model_provider** (`str`)
> LLM provider to use (e.g., OpenAI, Anthropic, Gemini). Example: `"openai"`

**model_name** (`str`)
> Model name to use for the agent. Example: `"gpt-4o-mini"`

**agent_name** (`str`)
> Name for the agent instance. Example: `"MoziChemAgent"`

**agent_prompt** (`str`)
> System prompt for agent behavior. Example: see `launch.py` for a template.

**mcp_source** (`dict`)
> MCP tool sources (API endpoints or remote configs). Example: see `launch.py` for details.

**memory_mode** (`bool`)
> Enable/disable agent memory (conversation history). Example: `True`

**open_browser** (`bool`)
> Automatically open browser UI when app starts. Example: `True`

### How to Set Arguments

- **Edit `examples/launch.py`**: Change values directly in the script before running.
- **Environment Variables**: API keys and some config (e.g., `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`) should be set in a `.env` file.
- **MCP Source**: You can configure MCP endpoints or remote tools by editing the `mcp_source` dictionary in `launch.py`.

### Example Usage

```python
mozichem_chat(
  model_provider="openai",
  model_name="gpt-4o-mini",
  agent_name="MoziChemAgent",
  agent_prompt="You are a helpful assistant...",
  mcp_source=None,  # or your MCP config
  memory_mode=True,
  open_browser=True,
)
```

Refer to `examples/launch.py` for a full template and customize as needed for your use case.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request to improve the project.

## 📝 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in your own applications or projects. However, if you choose to use this app in another app or software, please ensure that my name, Sina Gilassi, remains credited as the original author. This includes retaining any references to the original repository or documentation where applicable. By doing so, you help acknowledge the effort and time invested in creating this project.

## ❓ FAQ

For any questions, contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/).

## 👨‍💻 Authors

- [@sinagilassi](https://www.github.com/sinagilassi)