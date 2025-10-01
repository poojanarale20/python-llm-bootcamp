# Stateful Chatbot with Memory

A Python chatbot implementation that maintains conversation memory and user profiles using OpenAI's API and LangChain.

## Features

- **Session Memory**: Remembers conversations within sessions
- **User Profiles**: Stores user preferences and information
- **Conversation Summarization**: Automatically summarizes long conversations (>10 messages)
- **LangChain Integration**: Uses LangChain for memory management
- **OpenAI API**: Powered by GLM-4.5-Air via OpenRouter (configurable)
- **CLI Interface**: Interactive command-line interface
- **Programmatic API**: Easy to integrate into other applications

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up OpenRouter API Key

#### Option 1: Using .env file (Recommended)
```bash
# Copy the example environment file
cp env_example.txt .env

# The OpenRouter API key is already configured for GLM-4.5-Air model
# No additional setup needed!
```

#### Option 2: Environment variable
```bash
export OPENAI_API_KEY=your_openrouter_api_key_here
export MODEL_NAME=z-ai/glm-4.5-air:free
export BASE_URL=https://openrouter.ai/api/v1
```

## Usage

### Interactive CLI

```bash
python main.py
```

This will start an interactive chatbot session where you can:
- Chat with the bot
- Set user preferences
- View conversation history
- Clear memory
- Exit the session

#### CLI Commands

- `/profile` - Show user profile
- `/history` - Show conversation history
- `/info` - Show session information
- `/pref <key> <value>` - Set user preference
- `/clear` - Clear memory
- `/quit` - Exit chatbot

### Programmatic Usage

```python
from chatbot import StatefulChatbot

# Initialize chatbot
chatbot = StatefulChatbot()

# Start a session
chatbot.start_session("user123", "Alice")

# Set user preferences
chatbot.update_user_preference("user123", "favorite_color", "blue")
chatbot.update_user_preference("user123", "programming_language", "Python")

# Chat
response = chatbot.chat("Hello! What's my favorite color?")
print(response)

# Get conversation history
history = chatbot.get_conversation_history("user123")
print(f"Total messages: {len(history)}")

# Clear memory
chatbot.clear_memory("user123")
```

### Demo

Run the demo script to see all features in action:

```bash
python example.py
```

## Architecture

### Memory System

- **Session Memory**: `ConversationBufferWindowMemory` keeps last 10 messages
- **Summary Memory**: Automatically summarizes conversations >10 messages
- **User Profiles**: Persistent storage for user information and preferences

### Key Components

- **StatefulChatbot**: Main chatbot class
- **ConversationBufferWindowMemory**: Short-term memory
- **ConversationSummaryMemory**: Long-term memory with summarization
- **User profile management**: For personalization

### Example Conversation Flow

1. User starts session with name
2. Bot remembers user information
3. User sets preferences (e.g., favorite color, programming language)
4. Bot uses preferences in responses
5. After 10+ messages, conversation gets summarized
6. Bot maintains context across the session

## API Reference

### StatefulChatbot Class

#### Methods

- `start_session(session_id: str, user_name: Optional[str] = None) -> str`
  - Start a new conversation session
  
- `chat(message: str, session_id: Optional[str] = None) -> str`
  - Process a chat message and return response
  
- `get_user_profile(session_id: str) -> Optional[Dict]`
  - Retrieve user profile information
  
- `update_user_preference(session_id: str, key: str, value: str)`
  - Update user preference
  
- `get_conversation_history(session_id: Optional[str] = None) -> List[Dict]`
  - Get conversation history for a session
  
- `clear_memory(session_id: Optional[str] = None)`
  - Clear memory for a session
  
- `get_session_info(session_id: Optional[str] = None) -> Dict`
  - Get information about the current or specified session

#### Configuration

You can customize the chatbot by passing parameters to the constructor:

```python
chatbot = StatefulChatbot(
    api_key="your-api-key",           # Override API key
    model_name="gpt-4",              # Use different model
    base_url="https://api.openai.com/v1"  # Custom API endpoint
)
```

## Requirements

- Python 3.7+
- OpenRouter API key (already configured)
- Internet connection for API calls

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `langchain>=0.1.0` - LangChain framework
- `langchain-openai>=0.1.0` - LangChain OpenAI integration
- `python-dotenv>=1.0.0` - Environment variable management

## Files

- `chatbot.py` - Core chatbot implementation
- `main.py` - CLI interface
- `example.py` - Demo script
- `requirements.txt` - Python dependencies
- `env_example.txt` - Environment variable template
- `README.md` - This documentation

## Example Session

```
🤖 Stateful Chatbot with Memory
========================================
✅ Chatbot initialized successfully!

Enter session ID (or press Enter for 'default'): demo
Enter your name (optional): Alice

Session demo started. Hello Alice!

Commands:
  /profile - Show user profile
  /history - Show conversation history
  /info - Show session information
  /pref <key> <value> - Set user preference
  /clear - Clear memory
  /quit - Exit chatbot

Start chatting! (Type your message and press Enter)
----------------------------------------

You: Hello! What's my name?
Bot: Hello Alice! Your name is Alice.

You: /pref favorite_color blue
✅ Preference set: favorite_color = blue

You: What's my favorite color?
Bot: Your favorite color is blue, Alice!

You: /history
📜 Conversation History (3 messages):
  1. You: Hello! What's my name?
     Bot: Hello Alice! Your name is Alice.
  2. You: /pref favorite_color blue
     Bot: ✅ Preference set: favorite_color = blue
  3. You: What's my favorite color?
     Bot: Your favorite color is blue, Alice!

You: /quit
👋 Goodbye!
```

## License

This project is open source and available under the MIT License.
