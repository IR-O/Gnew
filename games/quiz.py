import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "correct": 1
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": 1
    },
    # Add more questions...
]

quiz_sessions = {}

def register(app):
    app.add_handler(CommandHandler('quiz', start_quiz))
    app.add_handler(CallbackQueryHandler(handle_quiz_answer, pattern='^quiz_'))

def start_quiz(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    question = random.choice(QUIZ_QUESTIONS)
    quiz_sessions[chat_id] = {
        "question": question,
        "score": 0
    }
    
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([InlineKeyboardButton(option, callback_data=f'quiz_{i}')])
    
    update.message.reply_text(
        question['question'],
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_quiz_answer(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    selected = int(query.data.split('_')[1])
    
    session = quiz_sessions.get(chat_id)
    if not session:
        query.answer()
        return
    
    question = session['question']
    if selected == question['correct']:
        session['score'] += 1
        query.edit_message_text(
            f"Correct! 🎉\nYour score: {session['score']}\n\n"
            "Want another question? /quiz"
        )
    else:
        correct_answer = question['options'][question['correct']]
        query.edit_message_text(
            f"Wrong! The correct answer was: {correct_answer}\n"
            f"Your score: {session['score']}\n\n"
            "Want another question? /quiz"
        )
    
    del quiz_sessions[chat_id]
    query.answer()