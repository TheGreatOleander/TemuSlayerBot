
"""
Setup Validator for TemuSlayerBot
Validates bot configuration and prerequisites
"""

import json
import os
import sys

def validate_config():
    """Validate bot configuration"""
    config_file = 'bot_config.json'
    
    if not os.path.exists(config_file):
        print("❌ No configuration file found.")
        print("   Run 'python main.py' to set up the bot.")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("❌ Configuration file is corrupted.")
        return False
    
    valid = True
    
    # Check bot token
    if not config.get('bot_token'):
        print("❌ Bot token is missing")
        valid = False
    else:
        print("✅ Bot token is configured")
    
    # Check channels
    channels = config.get('channels', [])
    if not channels:
        print("⚠️  No channels configured")
    else:
        print(f"✅ {len(channels)} channel(s) configured")
    
    # Check referral links
    referral_links = config.get('referral_links', [])
    if not referral_links:
        print("⚠️  No referral links configured")
    else:
        print(f"✅ {len(referral_links)} referral link(s) configured")
    
    # Check admin IDs
    admin_ids = config.get('admin_ids', [])
    if not admin_ids:
        print("⚠️  No admin IDs configured")
    else:
        print(f"✅ {len(admin_ids)} admin ID(s) configured")
    
    return valid

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = [
        'telegram',
        'flask', 
        'aiosqlite',
        'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def main():
    """Main validation function"""
    print("TemuSlayerBot - Setup Validator")
    print("=" * 40)
    
    print("\n📋 Checking configuration...")
    config_valid = validate_config()
    
    print("\n📦 Checking dependencies...")
    deps_valid = check_dependencies()
    
    print("\n" + "=" * 40)
    if config_valid and deps_valid:
        print("✅ Setup validation passed! Bot is ready to run.")
    else:
        print("❌ Setup validation failed. Please address the issues above.")
    
    return config_valid and deps_valid

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
