
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

A clean, modular LangChain-based AI agent with web search capabilities using Hugging Face models.

[Tech Doc](https://docs.google.com/document/d/1FpZ2sC_ca5Z3QjQ9dYS4br9D_5czdcmasgeMFf49rLI/edit?usp=sharing)

[Mermaid Diagram](https://www.mermaidchart.com/app/projects/cc5388e1-0eee-4d93-8a82-5b4c6064b61b/diagrams/237d9a95-8bab-41cc-8ca4-ebe099718d17/share/invite/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N1bWVudElEIjoiMjM3ZDlhOTUtOGJhYi00MWNjLThjYTQtZWJlMDk5NzE4ZDE3IiwiYWNjZXNzIjoiRWRpdCIsImlhdCI6MTc1NjU1MTI5NH0.hqDDEMDMo0YEyJU9JB-Ob8SxQSm1d4_L-obNqsbhSwA)

[Sync Doc of LegalCopilot app](https://docs.google.com/document/d/1-inhLvGuyQlD-xN2fdmA3N0cO2A3YLGTs4LhV9_HNeo/edit?usp=sharing)

## 🏗️ Architecture

The application is organized into modular components:

```
event-action-agent/
├── main.py          # Main entry point
├── config.py        # Configuration management
├── tools.py         # Web search tools and utilities
├── agent.py         # LangChain agent management
├── cli.py           # Command-line interface
├── prompts.py       # System prompt for the agent
├── requirements.txt # Dependencies
└── README.md        # This file
```

## 🚀 Features

- **Clean Modular Design**: Simple separation of concerns with dedicated modules
- **Web Search**: Real-time web search using DuckDuckGo
- **Hugging Face Integration**: Uses Hugging Face models via their API
- **Intelligent Agent**: Automatically decides when to search the web
- **Comprehensive Analysis**: Provides detailed summaries with key points and impacts
- **Simple CLI**: User-friendly command-line interface with examples

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

The application uses a centralized configuration system in `config.py`:

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

## 🛠️ Module Details

### config.py
- Centralized configuration management
- Environment variable handling
- Configuration validation

### tools.py
- Web search functionality using DuckDuckGo
- LangChain tool integration for the agent

### agent.py
- LangChain agent creation and management using `create_tool_calling_agent`
- Agent execution handling
- Integration with prompts module

### cli.py
- Command-line interface
- User interaction handling
- Example management
- Status display

### prompts.py
- System prompt for the LangChain agent
- Instructions for web search and analysis

### main.py
- Application entry point
- Clean, simple interface

## 🔧 Development

The modular structure makes it easy to:
- Add new tools and capabilities
- Modify configuration settings
- Extend the CLI interface
- Add new AI models or providers
- Implement additional search providers
- Customize prompts and templates

## 📝 Requirements

- Python 3.8+
- LangChain
- LangChain OpenAI
- LangChain Community
- DuckDuckGo Search
- python-dotenv (optional)