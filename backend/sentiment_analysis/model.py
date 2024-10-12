# backend/sentiment_analysis/model.py
from textblob import TextBlob

class SentimentAnalyzer:
    @staticmethod
    def analyze_sentiment(text: str) -> dict:
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return {'sentiment': 'positive', 'score': analysis.sentiment.polarity}
        elif analysis.sentiment.polarity == 0:
            return {'sentiment': 'neutral', 'score': 0}
        else:
            return {'sentiment': 'negative', 'score': analysis.sentiment.polarity}

# backend/sentiment_analysis/main.py
from model import SentimentAnalyzer
from database.db_manager import DBManager

def analyze_sentiments():
    db_manager = DBManager()
    cleaned_data = db_manager.get_cleaned_data()
    
    analyzed_data = []
    for item in cleaned_data:
        sentiment = SentimentAnalyzer.analyze_sentiment(item['cleaned_text'])
        analyzed_data.append({
            'id': item['id'],
            'sentiment': sentiment['sentiment'],
            'score': sentiment['score'],
            'created_at': item['created_at'],
            'user': item['user']
        })
    
    db_manager.store_analyzed_data(analyzed_data)

if __name__ == "__main__":
    analyze_sentiments()