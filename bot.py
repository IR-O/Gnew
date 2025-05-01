import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ContextTypes
)
from config import Config
from utils.database import db

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the telegram bot."""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later."
        )

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        "🎮 Welcome to Group Game Bot!\n\n"
        "Available commands:\n"
        "/start - Show this message\n"
        "/games - List available games\n"
        "/play [game] - Start a game\n"
        "/scores - Show leaderboard\n"
        "/help - Show help"
    )

async def list_games(update: Update, context: CallbackContext) -> None:
    """List available games."""
    await update.message.reply_text(
        "Available games:\n"
        "- trivia: Answer random questions\n"
        "- wordchain: Word chain game\n"
        "- quiz: Multiple choice quiz\n"
        "- tictactoe: Play Tic Tac Toe"
    )

async def play_game(update: Update, context: CallbackContext) -> None:
    """Start a game based on user input."""
    try:
        game_name = context.args[0].lower() if context.args else None
        
        if game_name == 'trivia':
            await start_trivia(update, context)
        elif game_name == 'wordchain':
            await start_wordchain(update, context)
        elif game_name == 'quiz':
            await start_quiz(update, context)
        elif game_name == 'tictactoe':
            await start_tictactoe(update, context)
        else:
            await update.message.reply_text("❌ Unknown game. Use /games to see available games.")
    except Exception as e:
        logger.error(f"Error in play_game: {e}")
        await update.message.reply_text("❌ An error occurred while starting the game.")

async def show_scores(update: Update, context: CallbackContext) -> None:
    """Show the leaderboard."""
    try:
        leaderboard = db.get_leaderboard()
        if not leaderboard:
            await update.message.reply_text("No scores yet! Be the first to play!")
            return
        
        sorted_scores = sorted(leaderboard.items(), key=lambda x: int(x[1]), reverse=True)[:10]
        response = "🏆 Leaderboard:\n\n" + "\n".join(
            f"{i+1}. User {user_id}: {score} points" 
            for i, (user_id, score) in enumerate(sorted_scores)
        )
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in show_scores: {e}")
        await update.message.reply_text("❌ Could not retrieve scores at this time.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle all non-command text messages."""
    if not update.message or not update.message.text:
        return
    
    try:
        chat_id = update.effective_chat.id
        if db.get_game_state(chat_id, 'trivia'):
            await check_trivia_answer(update, context)
        elif db.get_game_state(chat_id, 'wordchain'):
            await check_wordchain_answer(update, context)
        elif db.get_game_state(chat_id, 'tictactoe'):
            await handle_tictactoe_move(update, context)
        else:
            await update.message.reply_text("Type /games to see available games!")
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")

# Game implementations
async def start_trivia(update: Update, context: CallbackContext) -> None:
    """Start a trivia game."""
    try:
        chat_id = update.effective_chat.id
        question = "Sample question: What is the capital of France?"
        correct_answer = "Paris"
        
        db.set_game_state(chat_id, 'trivia', correct_answer)
        await update.message.reply_text(
            f"❓ TRIVIA: {question}\n\n"
            "Options:\n"
            "1. London\n"
            "2. Berlin\n"
            "3. Paris\n"
            "4. Madrid\n\n"
            "Reply with your answer!"
        )
    except Exception as e:
        logger.error(f"Error in start_trivia: {e}")
        await update.message.reply_text("❌ Could not start trivia game.")

async def check_trivia_answer(update: Update, context: CallbackContext) -> None:
    """Check the answer to a trivia question."""
    try:
        chat_id = update.effective_chat.id
        user_answer = update.message.text.strip()
        correct_answer = db.get_game_state(chat_id, 'trivia')
        
        if user_answer.lower() == correct_answer.lower():
            user_id = update.effective_user.id
            current_score = db.get_user_score(user_id)
            db.set_user_score(user_id, current_score + 10)
            await update.message.reply_text("✅ Correct! +10 points!")
        else:
            await update.message.reply_text(f"❌ Wrong! The correct answer was: {correct_answer}")
        
        db.set_game_state(chat_id, 'trivia', None)
    except Exception as e:
        logger.error(f"Error in check_trivia_answer: {e}")
        await update.message.reply_text("❌ Error processing your answer.")

async def start_tictactoe(update: Update, context: CallbackContext) -> None:
    """Start a Tic Tac Toe game."""
    try:
        chat_id = update.effective_chat.id
        game_state = {
            'board': [' '] * 9,
            'current_player': 'X'
        }
        db.set_game_state(chat_id, 'tictactoe', str(game_state))
        
        await update.message.reply_text(
            "⭕ TIC TAC TOE ⭕\n\n"
            "Board:\n"
            "1 | 2 | 3\n"
            "---------\n"
            "4 | 5 | 6\n"
            "---------\n"
            "7 | 8 | 9\n\n"
            "Player X's turn. Reply with a number (1-9) to make your move!"
        )
    except Exception as e:
        logger.error(f"Error in start_tictactoe: {e}")
        await update.message.reply_text("❌ Could not start Tic Tac Toe game.")

async def handle_tictactoe_move(update: Update, context: CallbackContext) -> None:
    """Handle a Tic Tac Toe move."""
    try:
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        move = update.message.text.strip()
        
        game_state = eval(db.get_game_state(chat_id, 'tictactoe'))
        
        # Validate move
        if not move.isdigit() or int(move) < 1 or int(move) > 9:
            await update.message.reply_text("❌ Please enter a number between 1-9")
            return
            
        pos = int(move) - 1
        if game_state['board'][pos] != ' ':
            await update.message.reply_text("❌ That position is already taken!")
            return
            
        # Make move
        game_state['board'][pos] = game_state['current_player']
        
        # Check for winner
        winner = check_winner(game_state['board'])
        if winner:
            await update.message.reply_text(f"🎉 Player {winner} wins!")
            db.set_game_state(chat_id, 'tictactoe', None)
            return
            
        # Switch player
        game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
        db.set_game_state(chat_id, 'tictactoe', str(game_state))
        
        # Display updated board
        board_str = format_tictactoe_board(game_state['board'])
        await update.message.reply_text(
            f"{board_str}\n\n"
            f"Player {game_state['current_player']}'s turn. Choose a position (1-9)"
        )
    except Exception as e:
        logger.error(f"Error in handle_tictactoe_move: {e}")
        await update.message.reply_text("❌ Invalid move or game error.")

def check_winner(board):
    """Check if there's a winner in Tic Tac Toe."""
    # Winning combinations
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def format_tictactoe_board(board):
    """Format the Tic Tac Toe board for display."""
    return (
        f"{board[0]} | {board[1]} | {board[2]}\n"
        "---------\n"
        f"{board[3]} | {board[4]} | {board[5]}\n"
        "---------\n"
        f"{board[6]} | {board[7]} | {board[8]}"
    )

def main() -> None:
    """Run the bot."""
    # Create the Application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Register handlers
    handlers = [
        CommandHandler("start", start),
        CommandHandler("games", list_games),
        CommandHandler("play", play_game),
        CommandHandler("scores", show_scores),
        CommandHandler("help", start),  # Reuse start as help
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
