import redis
from config import Config

class Database:
    def __init__(self):
        self.redis = redis.from_url(Config.REDIS_URL, decode_responses=True)
    
    def get_user_score(self, user_id: int) -> int:
        """Get user's current score."""
        return int(self.redis.hget('user_scores', str(user_id)) or 0
    
    def set_user_score(self, user_id: int, score: int) -> None:
        """Update user's score."""
        self.redis.hset('user_scores', str(user_id), score)
    
    def get_leaderboard(self) -> dict:
        """Get all scores."""
        return {k: int(v) for k, v in self.redis.hgetall('user_scores').items()}
    
    def get_game_state(self, chat_id: int, game_name: str) -> str:
        """Get current game state."""
        return self.redis.hget(f'game_states:{game_name}', str(chat_id))
    
    def set_game_state(self, chat_id: int, game_name: str, state: str) -> None:
        """Set game state."""
        if state is None:
            self.redis.hdel(f'game_states:{game_name}', str(chat_id))
        else:
            self.redis.hset(f'game_states:{game_name}', str(chat_id), state)

# Global database instance
db = Database()
