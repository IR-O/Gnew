import random
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackContext

WORDS = ['apple', 'brave', 'crane', 'dwarf', 'eagle', 'flame', 'grape', 'house']

wordle_games = {}

def register(app):
    app.add_handler(CommandHandler('wordle', start_wordle))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wordle_guess))

def start_wordle(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    wordle_games[chat_id] = {
        'word': random.choice(WORDS),
        'attempts': 0,
        'guesses': []
    }
    update.message.reply_text(
        "Wordle Game Started!\n"
        "Guess the 5-letter word. You have 6 attempts.\n"
        "Example guess: 'apple'"
    )

def handle_wordle_guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    game = wordle_games.get(chat_id)
    if not game:
        return
    
    guess = update.message.text.lower().strip()
    
    if len(guess) != 5 or not guess.isalpha():
        update.message.reply_text("Please enter a 5-letter word!")
        return
    
    game['attempts'] += 1
    game['guesses'].append(guess)
    
    if guess == game['word']:
        update.message.reply_text(
            f"🎉 Congratulations! You guessed the word in {game['attempts']} attempts!\n"
            f"{format_wordle_board(game)}\n\n"
            "Play again? /wordle"
        )
        del wordle_games[chat_id]
        return
    
    if game['attempts'] >= 6:
        update.message.reply_text(
            f"Game over! The word was: {game['word']}\n"
            f"{format_wordle_board(game)}\n\n"
            "Play again? /wordle"
        )
        del wordle_games[chat_id]
        return
    
    update.message.reply_text(
        f"Attempt {game['attempts']}/6\n"
        f"{format_wordle_board(game)}"
    )

def format_wordle_board(game):
    result = []
    for guess in game['guesses']:
        line = []
        for i, letter in enumerate(guess):
            if letter == game['word'][i]:
                line.append(f"🟩{letter}")
            elif letter in game['word']:
                line.append(f"🟨{letter}")
            else:
                line.append(f"⬛{letter}")
        result.append(' '.join(line))
    return '\n'.join(result)