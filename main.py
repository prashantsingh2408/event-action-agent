import json
import os
import sys
from typing import List, Dict, Any
from openai import OpenAI
from ddgs import DDGS

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, continue without it


def search_web(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo and return results as JSON string."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href") or r.get("url", ""),
                    "snippet": r.get("body", "")
                })
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Search failed: {str(e)}"})


def main():
    # Get API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY environment variable not found!")
        print("Please set it in your .env file or system environment:")
        print("   export GROQ_API_KEY=your_api_key_here")
        print("   or create a .env file with: GROQ_API_KEY=your_api_key_here")
        return

    # Get search query from command line arguments or use default
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        # Default examples - you can change these
        examples = [
            "new tax policies in India 2025",
            "latest legal updates in India",
            "OpenAI Open Model Hackathon 2025 deadline prizes",
            "new GST rules in India",
            "income tax changes 2025 India"
        ]
        print("🔍 Available search examples:")
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")
        print("\n💡 Or provide your own query as command line argument:")
        print("   python main.py 'your search query here'")
        
        choice = input("\nEnter number (1-5) or press Enter for default (1): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(examples):
            user_query = examples[int(choice) - 1]
        else:
            user_query = examples[0]  # Default to first example

    print(f"\n🔍 Searching for: {user_query}")

    # Initialize OpenAI client with Groq
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=api_key,
    )

    # Define the function schema for the model
    functions = [
        {
            "name": "search_web",
            "description": "Search the web for current information about a topic, event, or query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of search results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    ]

    # Start conversation
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can search the web for current information. When you need to find recent or specific information, use the search_web function."
        },
        {
            "role": "user",
            "content": f"Find current information about: {user_query}"
        }
    ]

    print("🤖 AI Agent: Let me search for that information...")
    
    # First call - model decides if it needs to search
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        functions=functions,
        function_call="auto"
    )

    response_message = response.choices[0].message

    # Check if the model wants to call a function
    if hasattr(response_message, 'function_call') and response_message.function_call:
        function_name = response_message.function_call.name
        function_args = json.loads(response_message.function_call.arguments)

        print(f"🔍 Function Call: {function_name} with args: {function_args}")

        # Call the function
        if function_name == "search_web":
            function_response = search_web(**function_args)

            print("📡 Search completed. Processing results...")

            # Create a new conversation with the search results
            analysis_messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes web search results and provides comprehensive summaries. Focus on the most recent and relevant information."
                },
                {
                    "role": "user",
                    "content": f"""Based on the following web search results about "{user_query}", provide a comprehensive summary:

Search Results:
{function_response}

Please provide:
1. Key details and main points
2. Important dates/deadlines (if applicable)
3. Changes or updates (if applicable)
4. How this affects people/businesses (if applicable)
5. Any notable requirements or restrictions (if applicable)

If the search results don't contain relevant information, please state that clearly and suggest what specific information would be helpful."""
                }
            ]

            # Get final response from the model
            final_response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=analysis_messages
            )

            print("\n" + "="*60)
            print("🤖 AI Response:")
            print("="*60)
            print(final_response.choices[0].message.content)
        else:
            print(f"❌ Unknown function: {function_name}")
    else:
        print("\n" + "="*60)
        print("🤖 AI Response (no function call needed):")
        print("="*60)
        print(response_message.content)


if __name__ == "__main__":
    main()