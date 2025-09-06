import sys
from typing import List

from ..agent import Config, LangChainAgent, notification_memory


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
    
    def show_memory_status(self):
        """Display the notification memory status."""
        print("🧠 Notification Memory Status:")
        print("=" * 40)
        stats = notification_memory.get_notification_stats()
        
        print(f"Total notifications: {stats['total_notifications']}")
        print(f"Recent notifications (7 days): {stats['recent_notifications']}")
        print(f"Notifications by topic: {stats['notifications_by_topic']}")
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
    
    def reset_memory(self):
        """Reset the notification memory."""
        print("🧠 Resetting notification memory...")
        notification_memory.reset_memory()
        print("✅ Notification memory has been reset.")
    
    def show_recent_notifications(self, topic: str = None, days: int = 7):
        """Show recent notifications."""
        if topic:
            print(f"📧 Recent notifications for '{topic}' (last {days} days):")
            notifications = notification_memory.get_recent_notifications(topic, days)
        else:
            print(f"📧 Recent notifications (last {days} days):")
            # Get notifications for all topics
            stats = notification_memory.get_notification_stats()
            notifications = []
            for topic_name in stats['notifications_by_topic'].keys():
                topic_notifications = notification_memory.get_recent_notifications(topic_name, days)
                notifications.extend(topic_notifications)
        
        if not notifications:
            print("   No recent notifications found.")
        else:
            for i, notif in enumerate(notifications, 1):
                print(f"   {i}. Topic: {notif['notification_data'].get('topic_searched', 'Unknown')}")
                print(f"      Sent at: {notif['sent_at']}")
                print(f"      Recipient: {notif['recipient']}")
                print(f"      Updates found: {len(notif['notification_data'].get('relevant_updates', []))}")
                print(f"      Reasoning: {notif['notification_data'].get('reasoning', 'N/A')}")
                # Show email subject/body preview if present
                email_content = notif['notification_data'].get('email_content') if isinstance(notif.get('notification_data'), dict) else None
                if isinstance(email_content, dict):
                    subject = email_content.get('subject')
                    body = email_content.get('body')
                    if subject:
                        print(f"      Email Subject: {subject}")
                    if body:
                        preview = body if len(body) <= 240 else body[:240] + "..."
                        print("      Email Body Preview:")
                        print("         " + preview.replace("\n", "\n         "))
                print()
    
    def run(self):
        """Main CLI execution method."""
        # Check for special commands
        if len(sys.argv) > 1:
            command = sys.argv[1]
            
            if command in ["--status", "-s"]:
                self.show_status()
                return
            
            elif command in ["--memory", "-m"]:
                self.show_memory_status()
                return
            
            elif command in ["--reset-memory", "-r"]:
                self.reset_memory()
                return
            
            elif command in ["--recent", "-rc"]:
                topic = sys.argv[2] if len(sys.argv) > 2 else None
                days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
                self.show_recent_notifications(topic, days)
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
            print("   python main.py --memory")
            print("   python main.py --reset-memory")
            print("   python main.py --recent [topic] [days]")
            print("   python main.py 'your query'")
            print("\n📝 Set your HF_TOKEN in .env file or environment variable:")
            print("   HF_TOKEN=your_huggingface_token")
