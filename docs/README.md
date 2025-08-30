
# Event Action Agent

```mermaid
---
config:
  layout: dagre
---
flowchart TB
    cron["Cron Job<br>- runs hourly/weekly"] --> n1["Agent"]

    n1 --> n2["Actions<br>- web search<br>- email send"]
    n1 --> n3["Capability<br>- if event (e.g. tax policy update) then run email action"]

    class cron,n1 rect;

```

A clean, modular LangChain-based AI agent with web search capabilities using Hugging Face models and intelligent notification memory system.

[Tech Doc](https://docs.google.com/document/d/1FpZ2sC_ca5Z3QjQ9dYS4br9D_5czdcmasgeMFf49rLI/edit?usp=sharing)

[Mermaid Diagram](https://www.mermaidchart.com/app/projects/cc5388e1-0eee-4d93-8a82-5b4c6064b61b/diagrams/237d9a95-8bab-41cc-8ca4-ebe099718d17/share/invite/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N1bWVudElEIjoiMjM3ZDlhOTUtOGJhYi00MWNjLThjYTQtZWJlMDk5NzE4ZDE3IiwiYWNjZXNzIjoiRWRpdCIsImlhdCI6MTc1NjU1MTI5NH0.hqDDEMDMo0YEyJU9JB-Ob8SxQSm1d4_L-obNqsbhSwA)

[Sync Doc of LegalCopilot app](https://docs.google.com/document/d/1-inhLvGuyQlD-xN2fdmA3N0cO2A3YLGTs4LhV9_HNeo/edit?usp=sharing)

## 🏗️ Architecture

The application is organized into modular components with a clean separation between the agent core and external interfaces:

```
event-action-agent/
├── main.py                    # Main entry point
├── cli.py                     # Command-line interface
├── run_tests.py              # Test runner (project root)
├── requirements.txt           # Dependencies
├── agent/                    # 🆕 Agent core package
│   ├── __init__.py           # Agent package exports
│   ├── agent.py              # LangChain agent management
│   ├── tools.py              # Web search tools and utilities
│   ├── prompts.py            # System prompt for the agent
│   ├── notification_memory.py # Notification memory system
│   └── config.py             # Configuration management
├── tests/                    # Test suite directory
│   ├── __init__.py           # Test package
│   ├── README.md             # Test documentation
│   ├── test_config.py        # Test configuration
│   ├── test_agent_integration.py  # Agent integration tests
│   ├── test_cli.py           # CLI functionality tests
│   ├── test_memory_system.py # Memory system tests
│   ├── test_memory_simple.py # Simple memory tests
│   ├── test_complete_system.py # End-to-end tests
│   └── run_tests.py          # Test runner (tests directory)
├── MEMORY_SYSTEM.md          # Memory system documentation
└── README.md                 # This file
```

## 🚀 Features

- **Clean Modular Design**: Simple separation of concerns with dedicated modules
- **Web Search**: Real-time web search using DuckDuckGo
- **Hugging Face Integration**: Uses Hugging Face models via their API
- **Intelligent Agent**: Automatically decides when to search the web
- **Comprehensive Analysis**: Provides detailed summaries with key points and impacts
- **Simple CLI**: User-friendly command-line interface with examples
- **🆕 Notification Memory**: Prevents duplicate email notifications
- **🆕 Comprehensive Testing**: Full test suite with unit, integration, and system tests
- **🆕 Scalable Architecture**: Agent core separated for future API development

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/event-action-agent.git
cd event-action-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Hugging Face token:
```bash
# Create a .env file
echo "HF_TOKEN=your_huggingface_token_here" > .env
```

## 🔧 Configuration

The application uses a centralized configuration system in `agent/config.py`:

- **HF_TOKEN**: Your Hugging Face API token
- **HF_BASE_URL**: Hugging Face API base URL
- **HF_MODEL**: Model to use (default: openai/gpt-oss-20b:together)
- **Agent Settings**: Max iterations, verbosity, etc.

## 🎯 Usage

### Interactive Mode
```bash
python main.py
```

### Direct Query Mode
```bash
python main.py "latest AI developments in 2025"
```

### Check Status
```bash
python main.py --status
```

### Memory Management
```bash
# View notification memory status
python main.py --memory

# View recent notifications
python main.py --recent

# View recent notifications for specific topic
python main.py --recent "tax policy"

# Reset notification memory (for testing)
python main.py --reset-memory
```

## 🧪 Testing

### Run All Tests
```bash
# From project root
python run_tests.py

# Or from tests directory
cd tests
python run_tests.py
```

### Run Individual Tests
```bash
# Run specific test file
python tests/test_memory_system.py
python tests/test_cli.py
python tests/test_agent_integration.py

# Run unit tests only
python -m unittest discover tests/ -p "test_*.py" -v
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **System Tests**: End-to-end workflow testing

## 📋 Examples

The application includes example queries you can try:
1. Latest AI developments in 2025
2. New tax policies in India 2025
3. OpenAI Open Model Hackathon 2025 deadline prizes
4. Latest news about artificial intelligence
5. Current developments in machine learning

## 🔍 How It Works

1. **Query Processing**: The agent receives your query and analyzes it
2. **Intelligent Decision**: The agent automatically decides if web search is needed
3. **Web Search**: If needed, performs real-time web search using DuckDuckGo
4. **AI Analysis**: Uses Hugging Face models to analyze and provide comprehensive responses
5. **🆕 Memory Check**: Checks notification memory to prevent duplicate emails
6. **🆕 Smart Notifications**: Only sends emails for new updates

## 🛠️ Module Details

### agent/ (Core Agent Package)
- **agent.py**: LangChain agent creation and management using `create_tool_calling_agent`
- **tools.py**: Web search functionality using DuckDuckGo and LangChain tool integration
- **prompts.py**: System prompt for the LangChain agent
- **notification_memory.py**: SQLite-based notification memory system
- **config.py**: Centralized configuration management
- **__init__.py**: Package exports for easy importing

### cli.py
- Command-line interface
- User interaction handling
- Example management
- Status display
- Memory management commands

### main.py
- Application entry point
- Clean, simple interface

### tests/
- Comprehensive test suite
- Unit, integration, and system tests
- Mocked external dependencies
- Automated test runner

## 🆕 Agent Package Usage

The agent core is now organized as a Python package for easy importing and future API development:

```python
# Import the agent package
from agent import LangChainAgent, search_web, checkIsMailneedtoSend, notification_memory

# Create and use the agent
agent = LangChainAgent()
result = agent.run("Your query here")

# Use individual tools
search_results = search_web.invoke({"query": "search term"})
email_decision = checkIsMailneedtoSend.invoke({"event_data": '{"topic": "test"}'})

# Use memory system
stats = notification_memory.get_notification_stats()
```

## 🆕 Notification Memory System

The system includes an intelligent notification memory system that:

- **Prevents Duplicates**: Uses idempotency keys to avoid duplicate emails
- **Tracks History**: Maintains complete notification history
- **Provides Statistics**: Offers insights into notification patterns
- **CLI Management**: Easy-to-use commands for memory management

See [MEMORY_SYSTEM.md](MEMORY_SYSTEM.md) for detailed documentation.

## 🧪 Testing

The project includes a comprehensive test suite:

- **20+ Unit Tests**: Covering all major components
- **Integration Tests**: Testing component interactions
- **System Tests**: End-to-end workflow validation
- **Mocked Dependencies**: No external API calls during testing

Run tests with:
```bash
python run_tests.py
```

## 🔄 Development

The modular structure makes it easy to:
- Add new tools and capabilities
- Modify configuration settings
- Extend the CLI interface
- Add new AI models or providers
- Implement additional search providers
- Customize prompts and templates
- **🆕 Create API endpoints** (future development)
- **🆕 Integrate with FastAPI** (future development)

## 📝 Requirements

- Python 3.8+
- LangChain
- LangChain OpenAI
- LangChain Community
- DuckDuckGo Search
- python-dotenv (optional)

## 🚀 Future Development

The new agent folder structure prepares the project for:

1. **API Development**: Easy to create FastAPI endpoints
2. **Microservices**: Agent can be deployed as a separate service
3. **Multiple Interfaces**: CLI, API, and web interfaces
4. **Scalability**: Better separation of concerns
5. **Testing**: Isolated agent testing