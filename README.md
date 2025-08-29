# Event Action Agent

A Python agent that uses OpenAI's function calling to automatically search the web and provide intelligent responses using Groq's API with the gpt-oss-20b model.

## Quick Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up API Key

**Option A: Create .env File**
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

**Option B: System Environment**
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

**Option C: Direct in Terminal**
```bash
GROQ_API_KEY=your_key_here python main.py
```

### 3. Get Your Groq API Key

1. Visit: https://console.groq.com/
2. Sign up for a free account
3. Generate your API key

## Usage

### Interactive Mode (with menu)
```bash
python main.py
```
Shows a menu with 5 pre-configured search examples to choose from.

### Direct Search
```bash
python main.py "new tax policies in India 2025"
python main.py "latest legal updates in India"
python main.py "GST rules changes 2025"
python main.py "OpenAI Open Model Hackathon 2025"
```

## Built-in Search Examples

The agent comes with pre-configured search examples:

1. **new tax policies in India 2025** - Latest tax law changes and reforms
2. **latest legal updates in India** - Recent legal developments and court decisions
3. **OpenAI Open Model Hackathon 2025 deadline prizes** - Tech events and competitions
4. **new GST rules in India** - GST policy updates and compliance changes
5. **income tax changes 2025 India** - Income tax reforms and new regulations

## Example Output

### Tax Policy Search Results

The agent successfully found and analyzed **New Income-Tax Law (India 2025)**:

**Key Changes:**
- Complete rewrite of 1961 Act
- 22% corporate tax rate option for new manufacturing units
- Simplified filing process with fewer sections

**Important Dates:**
- Presidential assent: August 2025
- Effective date: April 1, 2026
- Filing deadlines: October 15-31, 2025

**Impact on Businesses:**
- New 22% concessional tax rate with deduction restrictions
- Updated cryptocurrency and digital transaction rules
- Simplified compliance with unified digital platform

**Requirements:**
- Digital Tax ID (DT-ID) required
- New compliance portal for electronic filing
- Lowered audit threshold from ₹1Cr to ₹90Lac

## How It Works

1. **🤖 AI Analysis**: The AI model analyzes your query
2. **🔍 Function Calling**: Automatically decides to search the web if needed
3. **📡 Web Search**: Performs real-time DuckDuckGo search
4. **📊 Analysis**: Processes search results and provides structured summary
5. **📋 Output**: Delivers comprehensive analysis with key points, dates, and impacts

## Project Structure

```
event-action-agent/
├── main.py              # Main agent with function calling and flexible search
├── requirements.txt     # Python dependencies
├── .env                 # API key storage (optional)
├── README.md           # This file
└── .venv/              # Virtual environment (created during setup)
```

## Dependencies

- `openai>=1.102.0` - OpenAI API client
- `ollama>=0.3.0` - Local Ollama model support
- `ddgs>=8.1.0` - DuckDuckGo search integration
- `python-dotenv>=1.0.0` - Environment variable management

## Use Cases

### For Legal Professionals
- Stay updated on law changes and court decisions
- Monitor regulatory updates and compliance requirements
- Research current legal precedents and rulings

### For Business Owners
- Track tax policy changes and their impact
- Monitor regulatory updates affecting operations
- Stay informed about compliance deadlines

### For Tax Consultants
- Get current information on tax reforms
- Monitor policy changes and effective dates
- Research new compliance requirements

### For Researchers
- Get current information on any topic
- Monitor industry developments and trends
- Research policy changes and their implications

## Troubleshooting

### API Key Issues
```bash
❌ Error: GROQ_API_KEY environment variable not found!
```
**Solution**: Set the environment variable using one of the methods above.

### Import Errors
```bash
ModuleNotFoundError: No module named 'openai'
```
**Solution**: Activate virtual environment and install dependencies:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## References

- [OpenAI Open Model Hackathon](https://openai.devpost.com/)
- [OpenAI Function Calling Tutorial](https://www.datacamp.com/tutorial/open-ai-function-calling-tutorial)
- [Groq API Documentation](https://console.groq.com/)
- [DuckDuckGo Search](https://duckduckgo.com/)

# Links
- [Syncing doc](https://docs.google.com/document/d/1-inhLvGuyQlD-xN2fdmA3N0cO2A3YLGTs4LhV9_HNeo/edit?usp=sharing)
- [Tech Doc](https://docs.google.com/document/d/1FpZ2sC_ca5Z3QjQ9dYS4br9D_5czdcmasgeMFf49rLI/edit?usp=sharing)
- [Architecture diagram](https://www.mermaidchart.com/app/projects/cc5388e1-0eee-4d93-8a82-5b4c6064b61b/diagrams/237d9a95-8bab-41cc-8ca4-ebe099718d17/share/invite/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N1bWVudElEIjoiMjM3ZDlhOTUtOGJhYi00MWNjLThjYTQtZWJlMDk5NzE4ZDE3IiwiYWNjZXNzIjoiRWRpdCIsImlhdCI6MTc1NjM5NDc0Nn0.EQf-J2hvRjHTq9urHSljy9AhDoBCBZaKbZlzMYJP1q0)
