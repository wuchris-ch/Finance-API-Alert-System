#!/usr/bin/env python3
"""
Debug script to help identify Telegram bot issues
"""

import asyncio
import sys
import config
from telegram import Bot

async def debug_telegram():
    """Debug Telegram bot setup"""
    
    print("🔍 Telegram Bot Debug Information")
    print("=" * 50)
    
    bot = Bot(token=config.TELEGRAM_TOKEN)
    
    # Get bot info
    try:
        bot_info = await bot.get_me()
        print(f"🤖 Bot Username: @{bot_info.username}")
        print(f"🤖 Bot ID: {bot_info.id}")
        print(f"🤖 Bot Name: {bot_info.first_name}")
        print(f"🤖 Bot Link: https://t.me/{bot_info.username}")
    except Exception as e:
        print(f"❌ Error getting bot info: {e}")
        return
    
    print(f"\n📱 Your Chat ID: {config.TELEGRAM_CHAT_ID}")
    
    # Get updates to see if user has messaged the bot
    try:
        updates = await bot.get_updates()
        print(f"\n📨 Recent updates: {len(updates)} messages")
        
        if updates:
            print("\nRecent conversations:")
            for update in updates[-5:]:  # Show last 5 updates
                if update.message:
                    chat_id = update.message.chat.id
                    user_name = update.message.from_user.first_name if update.message.from_user else "Unknown"
                    text = update.message.text or "[No text]"
                    print(f"  Chat ID: {chat_id} | User: {user_name} | Message: {text[:30]}...")
        else:
            print("❌ No messages found!")
            print("\n🚨 SOLUTION: You need to:")
            print(f"1. Go to: https://t.me/{bot_info.username}")
            print("2. Click 'START' or send '/start'")
            print("3. Then run this script again")
            
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
    
    # Try to send a test message anyway
    print(f"\n🧪 Attempting to send test message to chat ID: {config.TELEGRAM_CHAT_ID}")
    try:
        await bot.send_message(
            chat_id=config.TELEGRAM_CHAT_ID,
            text="🎉 Debug test message!"
        )
        print("✅ Message sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        
        # Provide specific solutions based on error
        error_str = str(e).lower()
        if "chat not found" in error_str:
            print("\n💡 SOLUTION for 'Chat not found':")
            print(f"1. Open Telegram and go to: https://t.me/{bot_info.username}")
            print("2. Click the 'START' button")
            print("3. Send any message (like 'hello')")
            print("4. Run this script again")
        elif "forbidden" in error_str:
            print("\n💡 SOLUTION for 'Forbidden':")
            print("1. Make sure you've started the bot")
            print("2. Check if you blocked the bot")
            print("3. Try sending /start again")

if __name__ == "__main__":
    asyncio.run(debug_telegram()) 