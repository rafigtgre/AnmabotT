from flask import Flask, jsonify, request
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
app = Flask(__name__)

# --- Telegram Bot Handler ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online and ready!")

# --- Setup Async Telegram Bot ---
def start_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    asyncio.run(app_telegram.run_polling())

# --- Flask API route ---
@app.route("/api/animenosub")
def animenosub():
    q = request.args.get("q", "")
    return jsonify({"status": "working", "query": q})

# --- Start both Flask & Telegram ---
if __name__ == "__main__":
    import threading
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=8080)
    
