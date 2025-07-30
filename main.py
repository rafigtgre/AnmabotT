import os
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
bot = Bot(token=TOKEN)

def search_animenosub(query):
    url = f"https://animenosub.to/search?keyword={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    results = []
    for a in soup.select(".film_list-wrap .flw-item"):
        title = a.select_one(".film-name").text.strip()
        href = "https://animenosub.to" + a.select_one("a")["href"]
        thumb = a.select_one("img")["data-src"]
        results.append({"title": title, "url": href, "thumb": thumb})
    return results[:5]

@app.route("/api/animenosub")
def api_handler():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing 'q' param"}), 400
    results = search_animenosub(query)
    return jsonify(results)

async def animenosub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /get <anime name>")
        return
    query = " ".join(context.args)
    results = search_animenosub(query)
    if not results:
        await update.message.reply_text("No results found.")
        return
    for res in results:
        await update.message.reply_photo(
            photo=res["thumb"],
            caption=f"📺 {res['title']}\n🔗 {res['url']}"
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Animenosub Bot. Use /get <anime>")

def run_telegram_bot():
    app_telegram = ApplicationBuilder().token(TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("get", animenosub))
    app_telegram.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=PORT)
  
