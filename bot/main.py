import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import Update
from handlers.start import start, help_command, whoami
from handlers.person import person_command, handle_person_callback
from handlers.weight import weight_command, handle_weight_input
from handlers.meals import meal_command, handle_meal_callback, handle_meal_input
from handlers.summary import today_command, history_command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
WAITING_FOR = {}

def build_app():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is missing")
    app = Application.builder().token(token).build()
    app.bot_data["WAITING_FOR"] = WAITING_FOR
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("whoami", whoami))
    app.add_handler(CommandHandler("person", person_command))
    app.add_handler(CommandHandler("weight", weight_command))
    app.add_handler(CommandHandler("meal", meal_command))
    app.add_handler(CommandHandler("today", today_command))
    app.add_handler(CommandHandler("history", history_command))
    app.add_handler(CallbackQueryHandler(handle_person_callback, pattern=r"^person:"))
    app.add_handler(CallbackQueryHandler(handle_meal_callback, pattern=r"^mealtype:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_text))
    return app

async def route_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    waiting_for = context.application.bot_data.get("WAITING_FOR", {})
    chat_id = str(update.effective_chat.id)
    mode = waiting_for.get(chat_id)
    if mode == "weight":
        await handle_weight_input(update, context)
        return
    if isinstance(mode, str) and mode.startswith("meal:"):
        await handle_meal_input(update, context, mode.split(":", 1)[1])
        return
    await update.message.reply_text(
        "我还不确定你现在要记录什么\n\n"
        "可用指令:\n"
        "/person 选择身份\n"
        "/weight 记录体重\n"
        "/meal 记录饮食\n"
        "/today 查看今天\n"
        "/history 查看历史"
    )

if __name__ == "__main__":
    app = build_app()
    app.run_polling()
