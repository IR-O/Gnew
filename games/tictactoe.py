from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

# Game state storage
games = {}

def register(app):
    app.add_handler(CommandHandler('tictactoe', start_tictactoe))
    app.add_handler(CallbackQueryHandler(button_click, pattern='^ttt_'))

def start_tictactoe(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    games[chat_id] = {
        'board': [' ' for _ in range(9)],
        'current_player': 'X'
    }
    update.message.reply_text(
        'Tic Tac Toe - Player X starts',
        reply_markup=create_board(chat_id)
    )

def create_board(chat_id):
    board = games[chat_id]['board']
    keyboard = []
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(
                board[i+j] if board[i+j] != ' ' else ' ',
                callback_data=f'ttt_{i+j}'
            ))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    position = int(query.data.split('_')[1])
    
    game = games.get(chat_id)
    if not game or game['board'][position] != ' ':
        query.answer()
        return
    
    game['board'][position] = game['current_player']
    winner = check_winner(game['board'])
    
    if winner:
        query.edit_message_text(
            f"Player {winner} wins!",
            reply_markup=create_board(chat_id)
        )
        del games[chat_id]
    elif ' ' not in game['board']:
        query.edit_message_text(
            "It's a tie!",
            reply_markup=create_board(chat_id)
        )
        del games[chat_id]
    else:
        game['current_player'] = 'O' if game['current_player'] == 'X' else 'X'
        query.edit_message_text(
            f"Tic Tac Toe - Player {game['current_player']}'s turn",
            reply_markup=create_board(chat_id)
        )
    
    query.answer()

def check_winner(board):
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for line in lines:
        if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
            return board[line[0]]
    return None