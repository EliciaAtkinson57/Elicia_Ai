# Elicia AI Agent

A simple AI agent built with Python, OpenAI SDK, and Chainlit for the UI.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure your OpenAI API key:**
   - Open the `.env` file
   - Replace `your_api_key_here` with your actual OpenAI API key
   - Get your API key from: https://platform.openai.com/api-keys

3. **Run the agent with Chainlit UI:**
   ```bash
   chainlit run chainlit_app.py -w
   ```
   The `-w` flag enables auto-reload on file changes.

   Alternatively, run the CLI version:
   ```bash
   python agent.py
   ```

## Usage

### Chainlit UI (Recommended)
After running `chainlit run chainlit_app.py -w`, your browser will automatically open to `http://localhost:8000` where you can interact with the AI agent through a modern chat interface.

Features:
- Real-time streaming responses
- Clean, user-friendly interface
- Message history
- File upload support (configurable)

### CLI Version
The agent runs in an interactive chat mode. Simply type your messages and press Enter to get responses from the AI. Type `quit`, `exit`, or `q` to stop the agent.

## Project Structure

- `chainlit_app.py` - Chainlit web UI application (main entry point)
- `agent.py` - CLI version of the AI agent
- `.chainlit/config.toml` - Chainlit configuration
- `.env` - Configuration file for API keys (do not commit this!)
- `requirements.txt` - Python dependencies
- `.gitignore` - Prevents sensitive files from being committed

## Notes

- The default model is `gpt-4o-mini` (cost-effective and fast)
- You can change the model in `chainlit_app.py` or `agent.py`
- Never commit your `.env` file or share your API key
- Chainlit UI supports response streaming for a better user experience
