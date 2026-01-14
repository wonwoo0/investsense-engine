import os
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_message(message: str) -> bool:
    """
    Sends a message to the configured Telegram chat.

    Args:
        message (str): The text message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        return False
    if not TELEGRAM_CHAT_ID:
        print("Error: TELEGRAM_CHAT_ID not found in environment variables.")
        return False

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        # Use await with the coroutine
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown')
        print(f"Telegram message sent successfully to chat ID {TELEGRAM_CHAT_ID}.")
        return True
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # Example usage (for testing purposes)
    # This requires an active event loop for async functions
    import asyncio
    
    async def test_send():
        print("Attempting to send test message...")
        test_message = "🚀 Kazuha Invest Alert: Test message from notifier.py!"
        success = await send_telegram_message(test_message)
        if success:
            print("Test message sent.")
        else:
            print("Failed to send test message.")

    # To run the async test function
    # You need to set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in a .env file
    # or as environment variables.
    # Example .env:
    # TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
    # TELEGRAM_CHAT_ID="-YOUR_CHAT_ID" # Group chat IDs are usually negative
    
    # asyncio.run(test_send())
    print("\nTo test, uncomment the asyncio.run(test_send()) line and ensure .env variables are set.")
    print("For a quick manual test, ensure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are set,")
    print("then run this script with `python -c 'import asyncio; from notifier import send_telegram_message; asyncio.run(send_telegram_message(\"Hello Test\"))'`")