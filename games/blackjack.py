import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

blackjack_games = {}
CARD_VALUES = {
    'A': 11, '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10
}
SUITS = ['♠', '♥', '♦', '♣']

def register(app):
    app.add_handler(CommandHandler('blackjack', start_blackjack))
    app.add_handler(CallbackQueryHandler(handle_blackjack, pattern='^bj_'))

def start_blackjack(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    deck = create_deck()
    random.shuffle(deck)
    
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    blackjack_games[chat_id] = {
        'deck': deck,
        'player_hand': player_hand,
        'dealer_hand': dealer_hand,
        'state': 'player_turn'
    }
    
    keyboard = [
        [InlineKeyboardButton("Hit", callback_data='bj_hit')],
        [InlineKeyboardButton("Stand", callback_data='bj_stand')]
    ]
    
    update.message.reply_text(
        format_blackjack_state(chat_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def handle_blackjack(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_id = query.message.chat_id
    action = query.data.split('_')[1]
    
    game = blackjack_games.get(chat_id)
    if not game:
        query.answer()
        return
    
    if action == 'hit':
        game['player_hand'].append(game['deck'].pop())
        player_score = calculate_score(game['player_hand'])
        
        if player_score > 21:
            result = "Bust! You went over 21. Dealer wins!"
            del blackjack_games[chat_id]
            query.edit_message_text(
                f"{format_blackjack_state(chat_id)}\n\n{result}\n\nPlay again? /blackjack"
            )
            query.answer()
            return
    elif action == 'stand':
        game['state'] = 'dealer_turn'
        dealer_score = calculate_score(game['dealer_hand'])
        
        while dealer_score < 17:
            game['dealer_hand'].append(game['deck'].pop())
            dealer_score = calculate_score(game['dealer_hand'])
        
        player_score = calculate_score(game['player_hand'])
        
        if dealer_score > 21:
            result = "Dealer busts! You win!"
        elif dealer_score > player_score:
            result = "Dealer wins!"
        elif player_score > dealer_score:
            result = "You win!"
        else:
            result = "It's a tie!"
        
        del blackjack_games[chat_id]
        query.edit_message_text(
            f"{format_blackjack_state(chat_id, reveal=True)}\n\n{result}\n\nPlay again? /blackjack"
        )
        query.answer()
        return
    
    keyboard = [
        [InlineKeyboardButton("Hit", callback_data='bj_hit')],
        [InlineKeyboardButton("Stand", callback_data='bj_stand')]
    ]
    
    query.edit_message_text(
        format_blackjack_state(chat_id),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    query.answer()

def create_deck():
    deck = []
    for value in CARD_VALUES.keys():
        for suit in SUITS:
            deck.append(f"{value}{suit}")
    return deck

def calculate_score(hand):
    score = sum(CARD_VALUES[card[:-1]] for card in hand)
    aces = sum(1 for card in hand if card.startswith('A'))
    
    while score > 21 and aces:
        score -= 10
        aces -= 1
    
    return score

def format_blackjack_state(chat_id, reveal=False):
    game = blackjack_games[chat_id]
    player_cards = ' '.join(game['player_hand'])
    player_score = calculate_score(game['player_hand'])
    
    if reveal:
        dealer_cards = ' '.join(game['dealer_hand'])
        dealer_score = calculate_score(game['dealer_hand'])
        dealer_text = f"Dealer's cards: {dealer_cards} (Score: {dealer_score})"
    else:
        dealer_text = f"Dealer's cards: {game['dealer_hand'][0]} ??"
    
    return (
        f"Your cards: {player_cards} (Score: {player_score})\n"
        f"{dealer_text}\n\n"
        "Choose your action:"
    )