from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database.db_manager import DBManager
from backend.data_collection.collector import TwitterCollector

app = FastAPI()

# Configuration for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_manager = DBManager()
twitter_collector = TwitterCollector()

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API d'analyse de sentiments"}

@app.get("/api/sentiments")
async def get_sentiments():
    try:
        return db_manager.get_analyzed_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sentiments/summary")
async def get_sentiment_summary():
    try:
        data = db_manager.get_analyzed_data()
        positive = sum(1 for item in data if item['sentiment'] == 'positive')
        negative = sum(1 for item in data if item['sentiment'] == 'negative')
        neutral = sum(1 for item in data if item['sentiment'] == 'neutral')
        total = len(data)
        
        return {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "total": total
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/collect-tweets")
async def collect_and_store_data(query: str, count: int = 100):
    try:
        tweets = twitter_collector.collect_tweets(query, count)
        db_manager.store_raw_data(tweets)
        return {"message": f"Collected and stored {len(tweets)} tweets"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)