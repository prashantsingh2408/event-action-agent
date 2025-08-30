import sys
from typing import List

from config import Config
from agent import LangChainAgent


class CLI:
    """Command-line interface for the application."""
    
    def __init__(self):
        self.config = Config()
        self.examples = [
            "latest AI developments in 2025",
            "new tax policies in India 2025", 
            "OpenAI Open Model Hackathon 2025 deadline prizes",
            "latest news about artificial intelligence",
            "current developments in machine learning"
        ]
    
    def show_status(self):
        """Display the current configuration status."""
        print("🔧 Hugging Face Provider Status:")
        print("=" * 40)
        status = self.config.get_status()
        
        hf_status = "✅ Available" if status["huggingface"]["available"] else "❌ No API Key"
        print(f"HUGGINGFACE: {hf_status}")
        print(f"   API Key Env: {status['huggingface']['api_key_env']}")
        print(f"   Base URL: {status['huggingface']['base_url']}")
        print(f"   Model: {status['huggingface']['model']}")
        print()
    
    def show_examples(self):
        """Display available search examples."""
        print("🔍 Available example queries:")
        for i, example in enumerate(self.examples, 1):
            print(f"   {i}. {example}")
        print("\n💡 Or provide your own query as command line argument:")
        print("   python main.py 'your query here'")
    
    def get_user_query(self) -> str:
        """Get the user query from command line arguments or interactive input."""
        if len(sys.argv) > 1:
            return " ".join(sys.argv[1:])
        
        self.show_examples()
        choice = input("\nEnter number (1-5) or press Enter for default (1): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(self.examples):
            return self.examples[int(choice) - 1]
        else:
            return self.examples[0]  # Default to first example
    
    def run_agent(self, query: str):
        """Run the agent with the given query."""
        agent = LangChainAgent()
        
        print(f"🔍 Query: {query}")
        print("🤖 AI Agent: Processing your request...")
        
        # Run the agent
        result = agent.run(query)
        
        print("\n" + "="*60)
        print("🤖 AI Response:")
        print("="*60)
        print(result)
    
    def run(self):
        """Main CLI execution method."""
        # Check if user wants to see provider status
        if len(sys.argv) > 1 and sys.argv[1] in ["--status", "-s"]:
            self.show_status()
            return
        
        try:
            # Get user query
            user_query = self.get_user_query()
            
            # Run agent
            self.run_agent(user_query)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Available options:")
            print("   python main.py --status")
            print("   python main.py 'your query'")
            print("\n📝 Set your HF_TOKEN in .env file or environment variable:")
            print("   HF_TOKEN=your_huggingface_token")
