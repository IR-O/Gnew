from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    games_played = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    preferences = Column(JSON, default={})

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_user_stats(user_id):
    session = Session()
    stats = session.query(UserStats).filter_by(user_id=user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        session.add(stats)
        session.commit()
    return stats