from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import get_current_person, set_current_person

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    person = get_current_person(update.effective_chat.id)
    if not person:
        person = "Ji Hong"
        set_current_person(update.effective_chat.id, person)
    await update.message.reply_text(
        f"欢迎使用 Health Tracker\n\n"
        f"当前身份: {person}\n\n"
        f"可用指令:\n"
        f"/person 选择身份\n"
        f"/weight 记录体重\n"
        f"/meal 记录饮食\n"
        f"/today 查看今天\n"
        f"/history 查看最近记录\n"
        f"/whoami 查看 chat id"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"你的 chat id: {update.effective_chat.id}")
