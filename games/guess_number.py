import random
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext

guess_games = {}

def register(app):
    app.add_handler(CommandHandler('guess', start_guess))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))

def start_guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    guess_games[chat_id] = random.randint(1, 100)
    update.message.reply_text(
        "I'm thinking of a number between 1 and 100. Try to guess it!"
    )

def handle_guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    number = guess_games.get(chat_id)
    if not number:
        return
    
    try:
        guess = int(update.message.text)
    except ValueError:
        update.message.reply_text("Please enter a number!")
        return
    
    if guess < number:
        update.message.reply_text("Too low! Try again.")
    elif guess > number:
        update.message.reply_text("Too high! Try again.")
    else:
        update.message.reply_text(f"Congratulations! You guessed the number {number}!")
        del guess_games[chat_id]