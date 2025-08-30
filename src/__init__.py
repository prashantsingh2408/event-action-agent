"""
Event Action Agent Source Package.

Contains all the core functionality of the Event Action Agent.
"""

from .agent import LangChainAgent, search_web, checkIsMailneedtoSend, notification_memory, Config
from .cli import CLI

__version__ = "1.0.0"
__author__ = "Event Action Agent Team"

__all__ = [
    "LangChainAgent",
    "search_web", 
    "checkIsMailneedtoSend",
    "notification_memory",
    "Config",
    "CLI"
]
