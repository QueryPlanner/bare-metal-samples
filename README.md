# Open Services Agent Starter Pack

This repo is a **production-ready template** for building and deploying AI agents on your own infrastructure using **Google ADK**, **LiteLLM**, and **Postgres**.

It allows you to use the powerful Google ADK framework locally or on your own servers without being tied to Google Cloud services.

## Key Features

- 🐳 **Self-Hosted Ready**: Docker & Compose setup included. No GCP lock-in.
- 🧩 **Extensible**: Structured for adding Tools and Sub-Agents easily.
- 💾 **Persistent**: Postgres-backed sessions and conversation history.
- 🚀 **Modern Stack**: Python 3.11, `uv`, `fastapi`, `asyncpg`, `LiteLLM`.
- 🤖 **Multi-Model**: Use any provider (OpenRouter, OpenAI, Anthropic, etc.) via LiteLLM.

## Featured Example: Meme Agent

The repo comes with a fully functional **Meme Agent** (`agents/meme_agent`) that demonstrates:
- **Tool Usage**: Fetching images, getting meme information, and editing images.
- **Image Processing**: Adding text overlays with custom fonts (Impact).
- **Artifact Management**: Saving and loading generated images as ADK artifacts.

### Capabilities:
- `meme_info_tool`: Look up details about popular memes.
- `fetch_image_tool`: Retrieve meme templates from the local dataset.
- `add_text_to_image_tool`: Programmatically add top/bottom text to memes.
- `load_artifacts`: View and analyze generated content.

## Quickstart (Local Dev)

### Prerequisites

- Python **3.11+**
- [`uv`](https://github.com/astral-sh/uv)
- A Postgres connection string (Neon, local Postgres, etc.)
- An API key for your LLM provider (e.g., OpenRouter)

### 1) Configure environment

Create a `.env` file from the example:
```bash
cp .env.example .env
```
Edit `.env` and set:
- **`OPENROUTER_API_KEY`**: Your API key.
- **`DATABASE_URL`**: Your Postgres connection string.

### 2) Install dependencies

```bash
uv sync --extra dev
```

### 3) Run the Agent Platform

```bash
uv run python -m server
```

Then open `http://127.0.0.1:8000` to access the ADK Dev UI.

## Project Structure

- `server.py`: The main entrypoint that initializes the ADK FastAPI app with Postgres persistence.
- `agents/`: Directory where each subfolder is a separate agent.
- `platform_utils/`: Helpers for database URL normalization and environment management.
- `data/`: Local datasets (e.g., meme templates).
- `tests/`: Unit tests for tools and utilities.

## Customization

- **Add an Agent**: Create a new folder in `agents/` with an `agent.py` exporting `root_agent`.
- **Add Tools**: Define new functions in `agents/<your_agent>/tools/`.
- **Sub-agents**: Structure complex logic using the `sub_agents` pattern.

## Development & Quality

We maintain a "green build" policy. Before committing, run:

```bash
# Linting & Formatting
uv run ruff check .
uv run ruff format .

# Type Checking
uv run mypy .

# Testing
uv run pytest
```

## Deployment

For production deployment instructions, including systemd and Docker setup:

👉 **[Read the Deployment Guide](DEPLOYMENT.md)**

---

Built with [Google ADK](https://github.com/google/adk-python).