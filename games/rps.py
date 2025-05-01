import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

CHOICES = ['✊', '✋', '✌️']

def register(app):
    app.add_handler(CommandHandler('rps', start_rps))
    app.add_handler(CallbackQueryHandler(play_rps, pattern='^rps_'))

def start_rps(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("✊ Rock", callback_data='rps_0')],
        [InlineKeyboardButton("✋ Paper", callback_data='rps_1')],
        [InlineKeyboardButton("✌️ Scissors", callback_data='rps_2')]
    ]
    update.message.reply_text(
        "Choose your weapon:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def play_rps(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_choice = int(query.data.split('_')[1])
    bot_choice = random.randint(0, 2)
    
    result = determine_winner(user_choice, bot_choice)
    
    query.edit_message_text(
        f"You chose: {CHOICES[user_choice]}\n"
        f"I chose: {CHOICES[bot_choice]}\n\n"
        f"Result: {result}\n\n"
        "Play again? /rps"
    )
    query.answer()

def determine_winner(user, bot):
    if user == bot:
        return "It's a tie!"
    elif (user - bot) % 3 == 1:
        return "You win!"
    else:
        return "I win!"