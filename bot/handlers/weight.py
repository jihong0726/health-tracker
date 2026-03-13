from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.storage import add_weight, get_current_person
from utils.formatter import format_now_date, format_now_time

async def weight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["WAITING_FOR"][str(update.effective_chat.id)] = "weight"
    await update.message.reply_text("请输入体重，例如 72.4")

async def handle_weight_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    raw = update.message.text.strip().lower().replace("kg", "").strip()
    try:
        value = float(raw)
    except ValueError:
        await update.message.reply_text("体重格式不对，请输入数字，例如 72.4")
        return
    person = get_current_person(update.effective_chat.id)
    add_weight(person=person, value=value)
    context.application.bot_data["WAITING_FOR"].pop(chat_id, None)
    keyboard = [
        [InlineKeyboardButton("早餐", callback_data="mealtype:早餐")],
        [InlineKeyboardButton("午餐", callback_data="mealtype:午餐")],
        [InlineKeyboardButton("晚餐", callback_data="mealtype:晚餐")],
        [InlineKeyboardButton("宵夜", callback_data="mealtype:宵夜")],
    ]
    await update.message.reply_text(
        f"已记录\n"
        f"{person}\n"
        f"日期: {format_now_date()}\n"
        f"时间: {format_now_time()}\n"
        f"体重: {value:.1f} kg\n\n"
        f"记得补充今天吃了什么",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
