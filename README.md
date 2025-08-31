
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

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your Hugging Face token
echo "HF_TOKEN=your_huggingface_token_here" > .env

# Run the agent
python main.py
```

## 📚 Documentation

- **[Main Documentation](docs/README.md)** - Complete project overview and usage guide
- **[API Documentation](docs/API_README.md)** - API reference and integration guide
- **[Memory System](docs/MEMORY_SYSTEM.md)** - Notification memory system documentation
- **[Sample Events](docs/SAMPLE_EVENTS.md)** - Example events and use cases

## 🏗️ Project Structure

```
event-action-agent/
├── 📁 docs/                    # 📚 All documentation
│   ├── README.md              # Main documentation
│   ├── API_README.md          # API reference
│   ├── MEMORY_SYSTEM.md       # Memory system docs
│   └── SAMPLE_EVENTS.md       # Example events
├── 📁 src/                     # 🔧 Source code
│   ├── 📁 agent/              # Agent core package
│   └── 📁 cli/                # CLI interface
├── 📁 tests/                   # 🧪 Test suite
├── 📁 examples/                # 📝 Example scripts
├── 📁 scripts/                 # 🔨 Utility scripts
├── 📁 config/                  # ⚙️ Configuration files
├── main.py                     # 🚀 Main entry point
└── requirements.txt            # 📦 Dependencies
```

## 🎯 Features

- **🤖 Intelligent Agent**: LangChain-based AI agent with web search
- **🔍 Web Search**: Real-time search using DuckDuckGo
- **🧠 Memory System**: Prevents duplicate notifications
- **📊 Comprehensive Testing**: Full test suite
- **🔧 Modular Design**: Clean, scalable architecture
- **📚 Complete Documentation**: Extensive guides and examples

## 🧪 Testing

```bash
# Run all tests
python scripts/run_tests.py

# Run specific tests
python -m pytest tests/

# Check complete system test
python tests/test_complete_system.py
```

## 🔗 Links

- [Mermaid Diagram](https://www.mermaidchart.com/app/projects/cc5388e1-0eee-4d93-8a82-5b4c6064b61b/diagrams/237d9a95-8bab-41cc-8ca4-ebe099718d17/share/invite/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N1bWVudElEIjoiMjM3ZDlhOTUtOGJhYi00MWNjLThjYTQtZWJlMDk5NzE4ZDE3IiwiYWNjZXNzIjoiRWRpdCIsImlhdCI6MTc1NjU1MTI5NH0.hqDDEMDMo0YEyJU9JB-Ob8SxQSm1d4_L-obNqsbhSwA)
