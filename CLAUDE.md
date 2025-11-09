# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based AI agent that uses the OpenAI SDK to provide interactive chat functionality. The project has two interfaces:
1. **Chainlit UI** (primary) - Web-based chat interface with streaming responses
2. **CLI** (agent.py) - Command-line interface for terminal-based interaction

Both interfaces use the same OpenAI client configuration and model.

## Development Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the Chainlit UI (recommended):**
```bash
chainlit run chainlit_app.py -w
```
The `-w` flag enables watch mode for auto-reload during development. Opens browser at http://localhost:8000

**Run the CLI version:**
```bash
python agent.py
```

**Test the agent programmatically (for debugging):**
```python
python -c "from agent import chat_with_agent; print(chat_with_agent('Hello!'))"
```

## Architecture

**Core Components:**

- `chainlit_app.py` - Main Chainlit application with:
  - `@cl.on_chat_start`: Handler that runs when a new chat session starts, sends welcome message
  - `@cl.on_message`: Main message handler that processes user input and streams OpenAI responses
  - Streaming implementation using `client.chat.completions.create(stream=True)` for real-time token delivery

- `agent.py` - CLI version with:
  - `chat_with_agent()`: Core function that sends prompts to OpenAI API and returns responses
  - `main()`: Interactive CLI loop that processes user input and displays agent responses

- `.chainlit/config.toml` - Chainlit configuration:
  - UI settings (app name, theme, etc.)
  - Feature flags (file upload, prompt playground, etc.)
  - Session and security settings

**Configuration:**
- `.env` file contains `OPENAI_API_KEY`
- API key is loaded via `python-dotenv` and must be set before running
- Default model is `gpt-4o-mini` (can be changed in both `chainlit_app.py` and `agent.py`)

**Important:**
- The `.env` file is gitignored and must never be committed
- All OpenAI API calls go through the `client.chat.completions.create()` method
- Chainlit uses streaming responses for better UX
- Error handling is implemented in both interfaces to catch API failures

## Key Patterns

**When extending the Chainlit UI:**
- Add message handlers using `@cl.on_message` decorator
- Use `await msg.stream_token()` for streaming responses
- Use `@cl.on_chat_start` for initialization logic
- Store session state using `cl.user_session.set()` and `cl.user_session.get()`
- Modify system prompt in the messages list passed to OpenAI API

**When extending the CLI:**
- Add new capabilities by modifying the system message in `chat_with_agent()`
- For conversation history, maintain a messages list outside the function
- For different agent personas, create new functions with different system prompts

**General:**
- Always use environment variables for sensitive configuration
- Both interfaces share the same OpenAI client initialization pattern
- Keep the system prompt consistent between interfaces unless there's a specific reason to differ
