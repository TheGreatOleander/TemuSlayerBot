
"""
Configuration Manager for TemuSlayerBot
Utility to view and edit bot configuration
"""

import json
import os
import sys

def load_config():
    """Load bot configuration"""
    config_file = 'bot_config.json'
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No configuration file found. Run the main bot to set up.")
        return None

def display_config():
    """Display current configuration"""
    config = load_config()
    if not config:
        return
    
    print("\n--- Current Bot Configuration ---")
    print(f"Bot Username: {config.get('bot_username', 'Not set')}")
    print(f"Bot Token: {'*' * 20 if config.get('bot_token') else 'Not set'}")
    
    print(f"\nChannels ({len(config.get('channels', []))}):")
    for i, channel in enumerate(config.get('channels', []), 1):
        print(f"  {i}. {channel}")
    
    print(f"\nReferral Links ({len(config.get('referral_links', []))}):")
    for i, link in enumerate(config.get('referral_links', []), 1):
        print(f"  {i}. {link}")
    
    print(f"\nAdmin IDs ({len(config.get('admin_ids', []))}):")
    for i, admin_id in enumerate(config.get('admin_ids', []), 1):
        print(f"  {i}. {admin_id}")
    
    print(f"\nSettings:")
    print(f"  Auto-reply: {config.get('auto_reply', False)}")
    print(f"  Log Level: {config.get('log_level', 'INFO')}")

def main():
    """Main function for config manager"""
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        display_config()
    else:
        print("Usage: python config_manager.py show")
        print("  show - Display current configuration")

if __name__ == "__main__":
    main()
