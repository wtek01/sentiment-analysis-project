import tweepy
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterCollector:
    def __init__(self):
        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_KEY_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def collect_tweets(self, query: str, count: int = 100) -> List[Dict]:
        tweets = []
        for tweet in tweepy.Cursor(self.api.search_tweets, q=query, tweet_mode='extended').items(count):
            tweets.append({
                'id': tweet.id,
                'text': tweet.full_text,
                'created_at': tweet.created_at,
                'user': tweet.user.screen_name
            })
        return tweets