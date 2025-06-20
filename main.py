
#!/usr/bin/env python3
"""
TemuSlayerBot - Telegram L4L Automation Service
Main entry point for the bot application
"""

import asyncio
import logging
import os
import signal
import sys
from threading import Thread
import time
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class SetupWizard:
    def __init__(self):
        self.config_file = 'bot_config.json'
        
    def run_setup(self):
        """Run the interactive setup wizard"""
        print("\n" + "="*50)
        print("  TemuSlayerBot - Setup Wizard")
        print("="*50)
        
        if os.path.exists(self.config_file):
            print(f"\nExisting configuration found in {self.config_file}")
            response = input("Do you want to reconfigure? (y/N): ").strip().lower()
            if response != 'y':
                return self.load_config()
        
        config = {}
        
        # Bot Token Setup
        print("\n--- Bot Configuration ---")
        config['bot_token'] = input("Enter your Telegram Bot Token: ").strip()
        if not config['bot_token']:
            print("Error: Bot token is required!")
            return None
            
        config['bot_username'] = input("Enter your Bot Username (optional): ").strip() or "TemuSlayerBot"
        
        # Channel Setup
        print("\n--- Channel Configuration ---")
        channels = []
        print("Enter Telegram channels (one per line, press Enter on empty line to finish):")
        while True:
            channel = input("Channel ID or @username: ").strip()
            if not channel:
                break
            channels.append(channel)
        config['channels'] = channels
        
        # Referral Links Setup
        print("\n--- Referral Links Configuration ---")
        referral_links = []
        print("Enter referral links (one per line, press Enter on empty line to finish):")
        while True:
            link = input("Referral link: ").strip()
            if not link:
                break
            referral_links.append(link)
        config['referral_links'] = referral_links
        
        # Admin Settings
        print("\n--- Admin Configuration ---")
        admin_ids = []
        print("Enter admin user IDs (one per line, press Enter on empty line to finish):")
        while True:
            admin_id = input("Admin User ID: ").strip()
            if not admin_id:
                break
            try:
                admin_ids.append(int(admin_id))
            except ValueError:
                print("Invalid user ID, skipping...")
        config['admin_ids'] = admin_ids
        
        # Additional Settings
        print("\n--- Additional Settings ---")
        config['auto_reply'] = input("Enable auto-reply? (y/N): ").strip().lower() == 'y'
        config['log_level'] = input("Log level (INFO/DEBUG/WARNING/ERROR) [INFO]: ").strip().upper() or "INFO"
        
        # Save configuration
        self.save_config(config)
        print(f"\nConfiguration saved to {self.config_file}")
        return config
    
    def save_config(self, config):
        """Save configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

class TemuSlayerBot:
    def __init__(self, config=None):
        self.config = config or {}
        self.running = False
        self.web_thread = None
        
    async def start(self):
        """Start the bot application"""
        logger.info("Starting TemuSlayerBot...")
        self.running = True
        
        # Display configuration
        print("\n--- Bot Configuration ---")
        print(f"Bot Username: {self.config.get('bot_username', 'Not set')}")
        print(f"Channels: {len(self.config.get('channels', []))} configured")
        print(f"Referral Links: {len(self.config.get('referral_links', []))} configured")
        print(f"Admin IDs: {len(self.config.get('admin_ids', []))} configured")
        print(f"Auto-reply: {self.config.get('auto_reply', False)}")
        
        # Main bot loop
        while self.running:
            logger.info("Bot is running...")
            # Here you would implement your bot logic
            await asyncio.sleep(60)
    
    def stop(self):
        """Stop the bot application"""
        logger.info("Stopping TemuSlayerBot...")
        self.running = False

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)

async def main():
    """Main application entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run setup wizard
    setup = SetupWizard()
    config = setup.run_setup()
    
    if not config:
        logger.error("Setup failed or was cancelled")
        sys.exit(1)
    
    # Create and start bot with configuration
    bot = TemuSlayerBot(config)
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)
