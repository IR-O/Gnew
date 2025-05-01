import random
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def register(app):
    app.add_handler(CommandHandler('dice', roll_dice))

def roll_dice(update: Update, context: CallbackContext) -> None:
    dice = random.randint(1, 6)
    update.message.reply_text(f"🎲 You rolled a {dice}!")