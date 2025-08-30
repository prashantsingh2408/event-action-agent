import os
from typing import Optional

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, continue without it


class Config:
    """Configuration class for the application."""
    
    # Hugging Face Configuration
    HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
    HF_BASE_URL: str = "https://router.huggingface.co/v1"
    HF_MODEL: str = "openai/gpt-oss-20b:together"
    
    # Search Configuration
    DEFAULT_MAX_RESULTS: int = 5
    
    # Agent Configuration
    MAX_ITERATIONS: int = 20
    VERBOSE: bool = True
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.HF_TOKEN:
            raise ValueError("HF_TOKEN environment variable not found. Please set your Hugging Face token.")
        return True
    
    @classmethod
    def get_status(cls) -> dict:
        """Get current configuration status."""
        return {
            "huggingface": {
                "available": bool(cls.HF_TOKEN),
                "api_key_env": "HF_TOKEN",
                "base_url": cls.HF_BASE_URL,
                "model": cls.HF_MODEL
            }
        }
