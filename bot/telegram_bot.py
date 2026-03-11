import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv("API_BASE_URL")

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to JobSenseBot!\n\n"
        "Send your desired job role."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {"role": text}
        await update.message.reply_text(
            "Great! Now send your skills separated by commas.\n\nExample:\nPython, SQL, Data Analysis"
        )
    else:
        role = user_data[user_id]["role"]
        skills = text

        payload = {
            "skills": skills,
            "role": role
        }

        response = requests.post(f"{API_URL}/recommend", json=payload)
        jobs = response.json()

        message = "🔎 Top Job Matches:\n\n"

        for job in jobs:
            message += (
                f"💼 {job['job_title']}\n"
                f"⭐ Score: {job['similarity_score']}\n"
                f"{job['short_description']}\n\n"
            )

        await update.message.reply_text(message)

        del user_data[user_id]


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()