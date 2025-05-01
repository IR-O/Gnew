import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters

CROSSWORD_CLUES = [
    {
        "clue": "Programming language named after a snake",
        "answer": "python",
        "hint": "P _ _ _ _ N"
    },
    # Add more clues...
]

crossword_sessions = {}

def register(app):
    app.add_handler(CommandHandler('crossword', start_crossword))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_crossword_guess))

def start_crossword(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    clue = random.choice(CROSSWORD_CLUES)
    crossword_sessions[chat_id] = clue
    
    keyboard = [
        [InlineKeyboardButton("Get Hint", callback_data='crossword_hint')]
    ]
    
    update.message.reply_text(
        f"Crossword Clue: {clue['clue']}\n\n"
        "Guess the answer!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_crossword_guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    clue = crossword_sessions.get(chat_id)
    if not clue:
        return
    
    guess = update.message.text.lower().strip()
    if guess == clue['answer']:
        update.message.reply_text(
            f"✅ Correct! The answer is: {clue['answer']}\n\n"
            "Play another? /crossword"
        )
        del crossword_sessions[chat_id]
    else:
        update.message.reply_text("Not quite right. Try again!")

def handle_crossword_hint(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    clue = crossword_sessions.get(chat_id)
    if not clue:
        query.answer()
        return
    
    query.edit_message_text(
        f"Crossword Clue: {clue['clue']}\n\n"
        f"Hint: {clue['hint']}\n\n"
        "Guess the answer!"
    )
    query.answer()