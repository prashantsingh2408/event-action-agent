from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List
import json

from .config import Config
from .tools import search_web, checkIsMailneedtoSend, create_email_content
from .prompts import SystemPrompts


class LangChainAgent:
    """LangChain agent manager class."""
    
    def __init__(self):
        self.config = Config()
        self.config.validate_config()
        self.llm = self._create_llm()
        self.prompt = self._create_prompt()
        # Expose only tool-callable functions (LangChain @tool decorated)
        # create_email_content is a helper, not a tool, so we keep tools consistent
        self.tools = [search_web, checkIsMailneedtoSend]
        self.agent = self._create_agent()
        self.executor = self._create_executor()
    
    def _create_llm(self) -> ChatOpenAI:
        """Create the language model instance."""
        return ChatOpenAI(
            api_key=self.config.HF_TOKEN,
            model=self.config.HF_MODEL,
            base_url=self.config.HF_BASE_URL,
            temperature=0.1  # Lower temperature for more consistent tool usage
        )
    
    def _create_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for the agent."""
        return ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent."""
        return SystemPrompts.get_agent_system_prompt(self.config.HF_MODEL)
    
    def _create_agent(self):
        """Create the agent instance."""
        return create_tool_calling_agent(self.llm, self.tools, self.prompt)
    
    def _create_executor(self) -> AgentExecutor:
        """Create the agent executor."""
        return AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.config.VERBOSE,
            handle_parsing_errors=True,
            max_iterations=self.config.MAX_ITERATIONS,
            return_intermediate_steps=True  # Enable intermediate steps for debugging
        )
    
    def run(self, query: str) -> str:
        """Run the agent with a given query."""
        try:
            # Check if this is an update query - if so, handle it directly
            if self._is_update_query(query):
                return self._handle_update_query(query)
            
            # For other queries, use the normal agent flow
            result = self.executor.invoke({"input": query})
            
            if result.get("intermediate_steps"):
                print(f"Agent used {len(result['intermediate_steps'])} tools")
            
            return result["output"]
        except Exception as e:
            print(f"Agent execution error: {e}")
            try:
                response = self.llm.invoke(query)
                return response.content
            except Exception as e2:
                print(f"LLM fallback error: {e2}")
                return f"Error: {str(e)}"
    
    def _handle_update_query(self, query: str) -> str:
        """Handle update queries by calling both tools directly."""
        try:
            # Extract topic from query
            topic = self._extract_topic(query)
            
            # Call search_web tool
            search_result = search_web.invoke({"query": f"{topic} updates", "max_results": 5})
            
            # Call checkIsMailneedtoSend tool
            email_result = checkIsMailneedtoSend.invoke({"event_data": json.dumps({"topic": topic})})
            
            # Parse email decision
            try:
                email_data = json.loads(email_result)
                should_send = email_data.get("should_send_email", False)
                reasoning = email_data.get("reasoning", "No reasoning provided")
                email_content = email_data.get("email_content") or None
                
                if should_send:
                    email_status = "Will send email"
                else:
                    email_status = "Email already sent" if "already sent" in reasoning.lower() else "No need to send email"
            except:
                email_status = "Email decision unavailable"
                reasoning = "Could not parse email decision"
                email_content = None
            
            # Format response
            # Build response with optional email content section
            response = f"""**Search Results for {topic} updates:**
{search_result[:500]}...

**📧 Email Decision:** {email_status}
**Reasoning:** {reasoning}"""

            if email_content and isinstance(email_content, dict):
                subject = email_content.get("subject", "(no subject)")
                body = email_content.get("body", "(no body)")
                # Limit extremely long body display to keep terminal output readable
                preview_limit = 2000
                body_preview = body if len(body) <= preview_limit else body[:preview_limit] + "..."
                response += f"""

**✉️ Email Content:**
- **Subject:** {subject}

---
{body_preview}
---
"""
            
            return response
            
        except Exception as e:
            return f"Error handling update query: {str(e)}"
    
    def _extract_topic(self, query: str) -> str:
        """Extract topic from update query."""
        # Simple extraction - remove common words
        words_to_remove = ["there", "is", "any", "update", "updates", "in", "on", "about", "latest", "recent", "new"]
        words = query.lower().split()
        topic_words = [word for word in words if word not in words_to_remove]
        return " ".join(topic_words) if topic_words else "general"
    
    def _is_update_query(self, query: str) -> bool:
        """Check if the query is asking for updates."""
        update_keywords = ["update", "updates", "latest", "recent", "new", "changes"]
        return any(keyword in query.lower() for keyword in update_keywords)
    
    def _should_add_email_decision(self, result: dict) -> bool:
        """Check if we should add email decision to the response."""
        # Check if we have intermediate steps and if checkIsMailneedtoSend was called
        if result.get("intermediate_steps"):
            for step in result["intermediate_steps"]:
                if hasattr(step[0], 'tool') and step[0].tool == "checkIsMailneedtoSend":
                    return True
        return False
    
    def _add_email_decision_to_response(self, query: str, current_output: str, result: dict) -> str:
        """Add email decision to the response."""
        try:
            # Extract email decision from intermediate steps
            email_decision = None
            if result.get("intermediate_steps"):
                for step in result["intermediate_steps"]:
                    if hasattr(step[0], 'tool') and step[0].tool == "checkIsMailneedtoSend":
                        # Parse the tool output
                        tool_output = step[1]
                        if isinstance(tool_output, str):
                            try:
                                email_decision = json.loads(tool_output)
                            except:
                                pass
            
            if email_decision:
                # Add email decision to the response
                email_section = f"""

**📧 Email Notification Decision:**
- **Should send email:** {email_decision.get('should_send_email', 'Unknown')}
- **Reasoning:** {email_decision.get('reasoning', 'No reasoning provided')}
- **Topic searched:** {email_decision.get('topic_searched', 'Unknown')}
- **Relevant updates found:** {len(email_decision.get('relevant_updates', []))}

"""
                return current_output + email_section
            
        except Exception as e:
            print(f"Error adding email decision: {e}")
        
        return current_output
    
    def get_llm(self) -> ChatOpenAI:
        """Get the language model instance."""
        return self.llm
