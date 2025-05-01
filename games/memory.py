import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

memory_games = {}
EMOJIS = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮']

def register(app):
    app.add_handler(CommandHandler('memory', start_memory))
    app.add_handler(CallbackQueryHandler(handle_memory_click, pattern='^mem_'))

def start_memory(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    pairs = random.sample(EMOJIS, 6) * 2
    random.shuffle(pairs)
    
    memory_games[chat_id] = {
        'board': ['❓' for _ in range(12)],
        'solution': pairs,
        'flipped': [],
        'matched': set()
    }
    
    update.message.reply_text(
        "Memory Game - Find all matching pairs!",
        reply_markup=create_memory_board(chat_id)
    )

def create_memory_board(chat_id):
    game = memory_games[chat_id]
    keyboard = []
    for i in range(0, 12, 3):
        row = []
        for j in range(3):
            idx = i + j
            row.append(InlineKeyboardButton(
                game['board'][idx],
                callback_data=f'mem_{idx}'
            ))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def handle_memory_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    position = int(query.data.split('_')[1])
    
    game = memory_games.get(chat_id)
    if not game or position in game['matched'] or position in game['flipped']:
        query.answer()
        return
    
    game['board'][position] = game['solution'][position]
    game['flipped'].append(position)
    
    if len(game['flipped']) == 2:
        pos1, pos2 = game['flipped']
        if game['solution'][pos1] == game['solution'][pos2]:
            game['matched'].update([pos1, pos2])
            game['flipped'] = []
            if len(game['matched']) == 12:
                query.edit_message_text(
                    "Congratulations! You matched all pairs! 🎉\n"
                    "Play again? /memory"
                )
                del memory_games[chat_id]
                query.answer()
                return
        else:
            context.job_queue.run_once(
                lambda _: flip_back(chat_id, query.message.message_id, pos1, pos2),
                2.0
            )
    
    query.edit_message_text(
        "Memory Game - Find all matching pairs!",
        reply_markup=create_memory_board(chat_id)
    )
    query.answer()

def flip_back(chat_id, message_id, pos1, pos2):
    game = memory_games.get(chat_id)
    if not game:
        return
    
    game['board'][pos1] = '❓'
    game['board'][pos2] = '❓'
    game['flipped'] = []
    
    bot = memory_games['bot']
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Memory Game - Find all matching pairs!",
        reply_markup=create_memory_board(chat_id)
    )