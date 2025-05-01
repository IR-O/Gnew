import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from config import TOKEN
from games import (
    tictactoe, hangman, quiz, rps, dice, 
    guess_number, wordchain, memory, blackjack, 
    trivia, crossword, wordle
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm a game bot. Here are the games you can play:\n\n"
        "/tictactoe - Play Tic Tac Toe with friends\n"
        "/hangman - Play Hangman\n"
        "/quiz - Answer quiz questions\n"
        "/rps - Rock Paper Scissors\n"
        "/dice - Roll dice\n"
        "/guess - Guess the number\n"
        "/wordchain - Word chain game\n"
        "/memory - Memory matching game\n"
        "/blackjack - Play Blackjack\n"
        "/trivia - Trivia questions\n"
        "/crossword - Solve crossword clues\n"
        "/wordle - Play Wordle\n"
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Use /start to see all available games!")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Register commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Register game handlers
    tictactoe.register(application)
    hangman.register(application)
    quiz.register(application)
    rps.register(application)
    dice.register(application)
    guess_number.register(application)
    wordchain.register(application)
    memory.register(application)
    blackjack.register(application)
    trivia.register(application)
    crossword.register(application)
    wordle.register(application)

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()