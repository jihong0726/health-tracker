from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from utils.storage import set_current_person

async def person_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ji Hong", callback_data="person:Ji Hong")],
        [InlineKeyboardButton("Mabel", callback_data="person:Mabel")],
    ]
    await update.message.reply_text("请选择身份", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_person_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    person = query.data.split(":", 1)[1]
    set_current_person(update.effective_chat.id, person)
    await query.edit_message_text(f"已切换身份\n\n当前身份: {person}")
