import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 🔹 Replace with your actual Telegram Bot Token
TOKEN = "7214027935:AAFQ3JP7nRTihzIjJKRT8yRjJBESENHibJ4"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ✅ Log that the bot is running
logging.basicConfig(level=logging.INFO)
logging.info("✅ Bot is running and listening for commands...")

# 🛒 Handle /buy Command to Send Invoice
@dp.message_handler(commands=['buy'])
async def send_invoice(message: types.Message):
    user_id = message.from_user.id
    logging.info(f"💰 /buy command received from user {user_id}")

    # Call the invoice creation endpoint
    response = requests.post("https://your-render-server.com/create-invoice", json={"user_id": user_id})

    if response.status_code == 200:
        invoice_data = response.json()
        invoice_url = invoice_data.get("invoice_url", "")

        if invoice_url:
            await message.reply(f"🛍 Click below to purchase coins:\n[Pay with Telegram Stars]({invoice_url})", parse_mode="Markdown")
        else:
            await message.reply("❌ Failed to generate invoice. Try again later.")
    else:
        await message.reply("❌ Error connecting to payment server.")

# Start polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
