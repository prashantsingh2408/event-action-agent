from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List

from config import Config
from tools import search_web
from prompts import SystemPrompts


class LangChainAgent:
    """LangChain agent manager class."""
    
    def __init__(self):
        self.config = Config()
        self.config.validate_config()
        self.llm = self._create_llm()
        self.prompt = self._create_prompt()
        self.tools = [search_web]
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
            result = self.executor.invoke({"input": query})
            
            # Check if we have intermediate steps
            if result.get("intermediate_steps"):
                print(f"Agent used {len(result['intermediate_steps'])} tools")
            
            return result["output"]
        except Exception as e:
            print(f"Agent execution error: {e}")
            # Fallback: try direct LLM call
            try:
                response = self.llm.invoke(query)
                return response.content
            except Exception as e2:
                print(f"LLM fallback error: {e2}")
                return f"Error: {str(e)}"
    
    def get_llm(self) -> ChatOpenAI:
        """Get the language model instance."""
        return self.llm
