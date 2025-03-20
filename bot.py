import logging
import requests
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask

# 🔹 Replace with your actual Telegram Bot Token
TOKEN = "7214027935:AAFQ3JP7nRTihzIjJKRT8yRjJBESENHibJ4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ✅ Log that the bot is running
logging.basicConfig(level=logging.INFO)
logging.info("✅ Bot is running and listening for commands...")

# 🛒 Handle /buy Command to Send Invoice
@dp.message(Command("buy"))
async def send_invoice(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"💰 /buy command received from user {user_id}")

    # Call the invoice creation endpoint
    response = requests.post("https://python-payments-server.onrender.com/create-invoice", json={"user_id": user_id})

    if response.status_code == 200:
        invoice_data = response.json()
        invoice_url = invoice_data.get("invoice_url", "")

        if invoice_url:
            await message.answer(f"🛍 Click below to purchase coins:\n[Pay with Telegram Stars]({invoice_url})", parse_mode="Markdown")
        else:
            await message.answer("❌ Failed to generate invoice. Try again later.")
    else:
        await message.answer("❌ Error connecting to payment server.")

# ✅ Flask Web Server to Keep Render Running
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is Running!"

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    task1 = asyncio.create_task(dp.start_polling(bot))  # Run bot
    task2 = asyncio.to_thread(run_flask)  # Run Flask in a separate thread
    await asyncio.gather(task1, task2)

# ✅ Function to Start Flask Server
def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Render requires a port
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    asyncio.run(main())  # Run everything in a single event loop
