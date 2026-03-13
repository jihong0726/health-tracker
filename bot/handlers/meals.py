from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.storage import add_meal, get_current_person
from utils.formatter import format_now_date, format_now_time

async def meal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("早餐", callback_data="mealtype:早餐")],
        [InlineKeyboardButton("午餐", callback_data="mealtype:午餐")],
        [InlineKeyboardButton("晚餐", callback_data="mealtype:晚餐")],
        [InlineKeyboardButton("宵夜", callback_data="mealtype:宵夜")],
    ]
    await update.message.reply_text("请选择餐别", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_meal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    meal_type = query.data.split(":", 1)[1]
    context.application.bot_data["WAITING_FOR"][str(update.effective_chat.id)] = f"meal:{meal_type}"
    await query.edit_message_text(f"请输入{meal_type}内容")

async def handle_meal_input(update: Update, context: ContextTypes.DEFAULT_TYPE, meal_type: str):
    chat_id = str(update.effective_chat.id)
    content = update.message.text.strip()
    person = get_current_person(update.effective_chat.id)
    add_meal(person=person, meal_type=meal_type, content=content)
    context.application.bot_data["WAITING_FOR"].pop(chat_id, None)
    await update.message.reply_text(
        f"已记录\n"
        f"{person}\n"
        f"日期: {format_now_date()}\n"
        f"时间: {format_now_time()}\n"
        f"{meal_type}: {content}"
    )
