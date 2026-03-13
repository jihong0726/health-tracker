from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import get_current_person, get_today_data, get_recent_data
from utils.formatter import build_today_summary, build_history_summary

async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person = get_current_person(update.effective_chat.id)
    weights, meals = get_today_data(person)
    await update.message.reply_text(build_today_summary(person, weights, meals))

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person = get_current_person(update.effective_chat.id)
    weights, meals = get_recent_data(person, limit=7)
    await update.message.reply_text(build_history_summary(person, weights, meals))
