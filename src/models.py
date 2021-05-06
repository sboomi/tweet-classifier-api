from src import db
import datetime as dt

__all__ = [
    'Tweet'
]


class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    media_url = db.Column(db.String(200))
    tweet_date = db.Column(db.DateTime(), nullable=False,
                           default=dt.datetime.utcnow)
    twitter_id = db.Column(db.BigInteger, nullable=False, unique=True)
    handle = db.Column(db.String(15), nullable=False, unique=True)
    text = db.Column(db.Text(280), nullable=False)
    profile_user = db.Column(db.String(35), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    tweet_link = db.Column(db.String(65), nullable=False)
    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=dt.datetime.utcnow)
    _type = db.Column(db.String(15), nullable=False, default="tweet")

    def __repr__(self):
        return (f"{self.handle} posted, "
                f"the {self.timestamp.strftime('%Y-%m-%d')} "
                f"at {self.timestamp.strftime('%H:%M:%s')}, the following:\n"
                f"{self.text}")
