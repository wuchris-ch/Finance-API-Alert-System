# setup.py
# Quick setup script for the Stock Alert System

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def setup_project():
    """Main setup function"""
    print("🚀 Stock Alert System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Activate venv and install requirements
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    if not run_command(install_cmd, "Installing dependencies"):
        return False
    
    # Run demo to verify installation
    demo_cmd = f"{activate_cmd} && python demo.py"
    print("\n🎬 Running demo to verify installation...")
    if not run_command(demo_cmd, "Running demo"):
        return False
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Edit config.py to set your stock watchlist and thresholds")
    print("2. (Optional) Set up Telegram bot for notifications:")
    print("   - Message @BotFather to create a bot")
    print("   - Message @userinfobot to get your chat ID")
    print("   - Update TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in config.py")
    print("3. Run the system:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("   python alert_bot.py")
    print("\n📊 Useful commands:")
    print("   python demo.py          # Run demo with mock data")
    print("   python inspect_db.py    # View database contents")
    print("   python alert_bot.py     # Start monitoring")
    
    return True

if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1) 