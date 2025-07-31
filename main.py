import os
from dotenv import load_dotenv
from flask import Flask
from bot.dispatcher import setup_dispatcher
from api.routes import setup_routes

from telegram.ext import ApplicationBuilder

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup Flask app for Firebase API
flask_app = Flask(__name__)
setup_routes(flask_app)

# Setup Telegram bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    setup_dispatcher(app)
    print("Bot is running...")
    await app.run_polling()

# Run Flask and Telegram in parallel
if __name__ == "__main__":
    import asyncio
    import threading

    def run_flask():
        flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(main())
  
