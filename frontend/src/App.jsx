// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [sentiments, setSentiments] = useState([]);
  const [summary, setSummary] = useState({});

  useEffect(() => {
    fetchSentiments();
    fetchSummary();
  }, []);

  const fetchSentiments = async () => {
    const response = await axios.get('http://localhost:8000/api/sentiments');
    setSentiments(response.data);
  };

  const fetchSummary = async () => {
    const response = await axios.get('http://localhost:8000/api/sentiments/summary');
    setSummary(response.data);
  };

  return (
    <div className="App">
      <h1>Sentiment Analysis Dashboard</h1>
      <div>
        <h2>Summary</h2>
        <p>Positive: {summary.positive}</p>
        <p>Negative: {summary.negative}</p>
        <p>Neutral: {summary.neutral}</p>
        <p>Total: {summary.total}</p>
      </div>
      <div>
        <h2>Recent Sentiments</h2>
        <ul>
          {sentiments.slice(0, 10).map((sentiment) => (
            <li key={sentiment.id}>
              {sentiment.user_name}: {sentiment.sentiment} (Score: {sentiment.score})
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;