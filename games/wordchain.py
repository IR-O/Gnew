from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext

wordchain_games = {}

def register(app):
    app.add_handler(CommandHandler('wordchain', start_wordchain))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wordchain))

def start_wordchain(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    wordchain_games[chat_id] = {
        'last_word': None,
        'used_words': set()
    }
    update.message.reply_text(
        "Word Chain game started!\n"
        "Rules: Each new word must start with the last letter of the previous word.\n"
        "First player can say any word. Example: 'apple'"
    )

def handle_wordchain(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    game = wordchain_games.get(chat_id)
    if not game:
        return
    
    word = update.message.text.lower().strip()
    
    if not word.isalpha():
        update.message.reply_text("Please enter a valid word with letters only!")
        return
    
    if game['last_word']:
        last_letter = game['last_word'][-1]
        if word[0] != last_letter:
            update.message.reply_text(
                f"Your word must start with '{last_letter}'! Try again."
            )
            return
    
    if word in game['used_words']:
        update.message.reply_text("This word was already used! Try another one.")
        return
    
    game['used_words'].add(word)
    game['last_word'] = word
    update.message.reply_text(
        f"Good! Next word must start with '{word[-1]}'"
    )