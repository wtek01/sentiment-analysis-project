# backend/preprocessing/cleaner.py
import re
from typing import List

class TextCleaner:
    @staticmethod
    def clean_text(text: str) -> str:
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
        # Remove user mentions
        text = re.sub(r'@\w+', '', text)
        # Remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        return text.strip()

# backend/preprocessing/main.py
from cleaner import TextCleaner
from database.db_manager import DBManager

def preprocess_data():
    db_manager = DBManager()
    raw_data = db_manager.get_raw_data()
    
    cleaned_data = []
    for item in raw_data:
        cleaned_text = TextCleaner.clean_text(item['text'])
        cleaned_data.append({
            'id': item['id'],
            'cleaned_text': cleaned_text,
            'created_at': item['created_at'],
            'user': item['user']
        })
    
    db_manager.store_cleaned_data(cleaned_data)

if __name__ == "__main__":
    preprocess_data()