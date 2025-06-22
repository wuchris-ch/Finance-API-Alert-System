#!/usr/bin/env python3
"""
Simple script to test your Telegram bot configuration.
Run this after setting up your TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in config.py
"""

import asyncio
import sys
import config

try:
    from telegram import Bot
except ImportError:
    print("❌ python-telegram-bot not installed!")
    print("Run: pip install python-telegram-bot")
    sys.exit(1)

async def test_telegram_bot():
    """Test if Telegram bot is configured correctly"""
    
    print("🤖 Testing Telegram Bot Configuration...")
    print("=" * 50)
    
    # Check if credentials are configured
    if config.TELEGRAM_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ TELEGRAM_TOKEN not configured!")
        print("Please update TELEGRAM_TOKEN in config.py with your bot token from @BotFather")
        return False
        
    if config.TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("❌ TELEGRAM_CHAT_ID not configured!")
        print("Please update TELEGRAM_CHAT_ID in config.py with your chat ID from @userinfobot")
        return False
    
    print(f"✅ Token configured: {config.TELEGRAM_TOKEN[:10]}...")
    print(f"✅ Chat ID configured: {config.TELEGRAM_CHAT_ID}")
    
    # Test bot initialization
    try:
        bot = Bot(token=config.TELEGRAM_TOKEN)
        print("✅ Bot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        print("Check if your TELEGRAM_TOKEN is correct")
        return False
    
    # Test getting bot info
    try:
        bot_info = await bot.get_me()
        print(f"✅ Bot info retrieved: @{bot_info.username}")
    except Exception as e:
        print(f"❌ Failed to get bot info: {e}")
        print("Check your internet connection and bot token")
        return False
    
    # Test sending a message
    try:
        test_message = "🎉 Test message from your Stock Alert System!\n\nIf you see this, Telegram notifications are working perfectly! 🚀"
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text=test_message,
            parse_mode="Markdown"
        )
        print("✅ Test message sent successfully!")
        print("Check your Telegram to see the test message.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test message: {e}")
        print("\nPossible issues:")
        print("1. Chat ID is incorrect")
        print("2. You haven't started a conversation with your bot yet")
        print("3. Bot doesn't have permission to message you")
        print("\nSolutions:")
        print("1. Double-check your chat ID from @userinfobot")
        print("2. Send /start to your bot first")
        print("3. Make sure the chat ID format is correct (can be negative for groups)")
        return False

def main():
    """Main function to run the test"""
    try:
        success = asyncio.run(test_telegram_bot())
        
        if success:
            print("\n🎉 SUCCESS! Your Telegram bot is configured correctly!")
            print("You can now run 'python alert_bot.py' to start receiving stock alerts.")
        else:
            print("\n❌ Configuration incomplete. Please fix the issues above.")
            
    except KeyboardInterrupt:
        print("\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    main() 