import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

TRIVIA_QUESTIONS = [
    {
        "question": "Which country is home to the kangaroo?",
        "options": ["Canada", "Australia", "Brazil", "South Africa"],
        "correct": 1,
        "category": "Geography"
    },
    # Add more questions...
]

trivia_sessions = {}

def register(app):
    app.add_handler(CommandHandler('trivia', start_trivia))
    app.add_handler(CallbackQueryHandler(handle_trivia_answer, pattern='^trivia_'))

def start_trivia(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    question = random.choice(TRIVIA_QUESTIONS)
    trivia_sessions[chat_id] = question
    
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'trivia_{i}')])
    
    update.message.reply_text(
        f"Category: {question['category']}\n\n"
        f"Question: {question['question']}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_trivia_answer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    selected = int(query.data.split('_')[1])
    
    question = trivia_sessions.get(chat_id)
    if not question:
        query.answer()
        return
    
    if selected == question['correct']:
        result = "✅ Correct! Well done!"
    else:
        correct_answer = question['options'][question['correct']]
        result = f"❌ Wrong! The correct answer was: {correct_answer}"
    
    query.edit_message_text(
        f"{result}\n\n"
        "Play again? /trivia"
    )
    query.answer()