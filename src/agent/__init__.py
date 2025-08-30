"""
Event Action Agent Package

A modular LangChain-based AI agent with web search capabilities and intelligent notification memory.
"""

from .agent import LangChainAgent
from .tools import search_web, checkIsMailneedtoSend
from .notification_memory import notification_memory
from .config import Config

__version__ = "1.0.0"
__author__ = "Event Action Agent Team"

__all__ = [
    "LangChainAgent",
    "search_web", 
    "checkIsMailneedtoSend",
    "notification_memory",
    "Config"
]
