
"""
Configuration management for TemuSlayerBot
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Bot configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN', '')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'TemuSlayerBot')
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///temuslayer.db')
    
    # Web interface configuration
    WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
    WEB_PORT = int(os.getenv('WEB_PORT', 5000))
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")
        
        return True
