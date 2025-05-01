import random
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext

hangman_games = {}
WORDS = ['python', 'telegram', 'hangman', 'developer', 'keyboard', 'internet', 'gaming', 'programming']

def register(app):
    app.add_handler(CommandHandler('hangman', start_hangman))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hangman_guess))

def start_hangman(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    word = random.choice(WORDS).lower()
    hangman_games[chat_id] = {
        'word': word,
        'guessed': set(),
        'attempts': 6
    }
    update.message.reply_text(
        f"Let's play Hangman! Guess the word: {display_word(chat_id)}\n"
        f"Attempts left: 6\n"
        "Guess a letter or the whole word!"
    )

def handle_hangman_guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    game = hangman_games.get(chat_id)
    if not game:
        return
    
    guess = update.message.text.lower()
    word = game['word']
    
    if len(guess) == 1 and guess.isalpha():
        if guess in game['guessed']:
            update.message.reply_text("You already guessed that letter!")
            return
        game['guessed'].add(guess)
        if guess not in word:
            game['attempts'] -= 1
    elif len(guess) == len(word) and guess.isalpha():
        if guess == word:
            update.message.reply_text(f"Congratulations! You guessed the word: {word}")
            del hangman_games[chat_id]
            return
        else:
            game['attempts'] -= 1
    else:
        update.message.reply_text("Please enter a single letter or the whole word!")
        return
    
    displayed = display_word(chat_id)
    if displayed == word:
        update.message.reply_text(f"Congratulations! You guessed the word: {word}")
        del hangman_games[chat_id]
    elif game['attempts'] <= 0:
        update.message.reply_text(f"Game over! The word was: {word}")
        del hangman_games[chat_id]
    else:
        update.message.reply_text(
            f"{displayed}\n"
            f"Attempts left: {game['attempts']}\n"
            f"Guessed letters: {', '.join(sorted(game['guessed']))}"
        )

def display_word(chat_id):
    game = hangman_games[chat_id]
    return ' '.join(
        letter if letter in game['guessed'] else '_'
        for letter in game['word']
    )