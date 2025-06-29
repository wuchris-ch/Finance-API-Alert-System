# setup.py
# Quick setup script for the Stock Alert System using uv

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

def check_uv_installed():
    """Check if uv is installed"""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ uv is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv is not installed. Please install uv first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   or visit: https://docs.astral.sh/uv/getting-started/installation/")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version {version.major}.{version.minor} is compatible")
    return True

def setup_project():
    """Main setup function"""
    print("🚀 Stock Alert System Setup (using uv)")
    print("=" * 40)
    
    # Check if uv is installed
    if not check_uv_installed():
        return False
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Initialize uv project if not already done
    if not Path("uv.lock").exists():
        if not run_command("uv sync", "Initializing uv project and installing dependencies"):
            return False
    else:
        print("✅ uv project already initialized")
        if not run_command("uv sync", "Syncing dependencies"):
            return False
    
    # Run demo to verify installation
    print("\n🎬 Running demo to verify installation...")
    if not run_command("uv run python demos/demo.py", "Running demo"):
        print("⚠️  Demo failed, but dependencies are installed. You may need to configure the system first.")
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\n📋 Next steps:")
    print("1. Configure your environment variables in .env file")
    print("2. Set up your database:")
    print("   uv run setup-db")
    print("3. (Optional) Set up Telegram bot for notifications:")
    print("   - Message @BotFather to create a bot")
    print("   - Message @userinfobot to get your chat ID")
    print("   - Add TELEGRAM_TOKEN and TELEGRAM_CHAT_ID to .env file")
    print("4. Run the system:")
    print("   uv run alert-bot")
    print("\n📊 Useful commands:")
    print("   uv run python demos/demo.py    # Run demo with mock data")
    print("   uv run inspect-db              # View database contents")
    print("   uv run alert-bot               # Start monitoring")
    print("   uv run python main.py          # Alternative entry point")
    print("\n🔧 Development commands:")
    print("   uv add <package>               # Add new dependency")
    print("   uv remove <package>            # Remove dependency")
    print("   uv sync                        # Sync dependencies")
    print("   uv run pytest                 # Run tests")
    
    return True

if __name__ == "__main__":
    success = setup_project()
    sys.exit(0 if success else 1)