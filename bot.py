import logging
import requests
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from flask import Flask
from threading import Thread

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

# ✅ Start polling properly
async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# ✅ Flask Web Server to Keep Render Running
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Telegram Bot is Running!"

# ✅ Run Flask Server and Start Bot in Background
def run_flask():
    port = int(os.environ.get("PORT", 8080))  # Render requires a port
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start bot in a separate thread
    Thread(target=lambda: asyncio.run(start_bot()), daemon=True).start()
    
    # Start Flask server (keeps Render active)
    run_flask()
