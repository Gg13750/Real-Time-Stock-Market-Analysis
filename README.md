# Real-Time Stock Market Sentiment Analysis

A simple yet impressive software engineering project that combines stock market data with sentiment analysis to provide insights into market sentiment for any publicly traded stock.

## 🚀 Features

- **Real-time Stock Data**: Fetches live stock prices, market cap, and volume using Yahoo Finance API
- **News Sentiment Analysis**: Analyzes recent news headlines using TextBlob NLP library
- **Interactive Visualizations**: Beautiful charts and gauges using Plotly
- **Sentiment Timeline**: Track how sentiment changes over time
- **Multiple Stock Support**: Analyze any stock ticker symbol
- **Responsive Web Interface**: Clean, professional Streamlit dashboard

## 📊 What the App Shows

1. **Stock Price Metrics**: Current price, price change, market cap, volume
2. **Price Chart**: Interactive line chart showing stock price movement
3. **Sentiment Gauge**: Visual gauge showing overall sentiment score (-1 to +1)
4. **Sentiment Distribution**: Pie chart of positive/negative/neutral news
5. **News Headlines Table**: Recent news with sentiment scores
6. **Sentiment Timeline**: Scatter plot showing sentiment changes over time

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download the Project
Create a new folder and save both files (`stock_sentiment_app.py` and `requirements.txt`) in it.

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv sentiment_env
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
sentiment_env\Scripts\activate
```

**Mac/Linux:**
```bash
source sentiment_env/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Download TextBlob Corpora (One-time setup)
```bash
python -m textblob.download_corpora
```

## 🚀 How to Run

1. Make sure your virtual environment is activated
2. Run the Streamlit app:
```bash
streamlit run stock_sentiment_app.py
```

3. Open your web browser and go to: `http://localhost:8501`

## 💡 How to Use

1. **Enter Stock Symbol**: In the sidebar, type any stock ticker (e.g., AAPL, GOOGL, TSLA, MSFT)
2. **Select Time Period**: Choose analysis period (1 day, 5 days, 1 month, 3 months)
3. **View Results**: The app will automatically fetch data and display:
   - Current stock metrics
   - Price chart
   - Sentiment analysis of recent news
   - Overall sentiment score and distribution

## 🎯 Project Highlights for Demonstration

### Technical Skills Demonstrated:
- **Web Development**: Streamlit framework for responsive web apps
- **Data Analysis**: Pandas and NumPy for data manipulation
- **API Integration**: Yahoo Finance API for real-time financial data
- **Natural Language Processing**: TextBlob for sentiment analysis
- **Data Visualization**: Interactive charts with Plotly
- **Caching**: Smart data caching for performance optimization

### Software Engineering Best Practices:
- Clean, modular code structure
- Error handling and user feedback
- Caching for performance optimization
- Professional UI/UX design
- Documentation and comments

## 📈 Example Use Cases

1. **Investment Research**: Gauge market sentiment before making investment decisions
2. **News Impact Analysis**: See how recent news affects stock sentiment
3. **Market Monitoring**: Track sentiment changes over time for multiple stocks
4. **Educational Tool**: Learn about the relationship between news sentiment and stock performance

## 🔧 Customization Options

- **Add More News Sources**: Extend news fetching to include more financial news APIs
- **Advanced Sentiment Models**: Replace TextBlob with more sophisticated NLP models
- **Technical Indicators**: Add moving averages, RSI, or other technical analysis
- **Alert System**: Add email/SMS alerts for significant sentiment changes
- **Database Integration**: Store historical sentiment data for trend analysis

## 📝 Future Enhancements

1. **Social Media Integration**: Include Twitter/Reddit sentiment
2. **Machine Learning**: Train custom models on financial text
3. **Portfolio Analysis**: Analyze sentiment for entire stock portfolios
4. **Predictive Modeling**: Correlate sentiment with future stock performance
5. **Mobile App**: Convert to mobile-friendly format

## 🎓 Educational Value

This project demonstrates:
- **Financial Technology (FinTech)** application development
- **Data Science** pipeline from data collection to visualization
- **Web Application** development with modern frameworks
- **API Integration** and real-time data processing
- **Natural Language Processing** in financial contexts

## ⚠️ Important Notes

- This is for educational purposes only and should not be used as the sole basis for investment decisions
- Sentiment analysis results are approximations and may not reflect true market conditions
- Always do thorough research before making any investment decisions

## 📊 Sample Output

When you run the app with AAPL (Apple), you'll see:
- Current Apple stock price and changes
- Recent Apple news headlines with sentiment scores
- Visual gauge showing overall sentiment
- Timeline of how sentiment changed throughout recent news
- Interactive charts showing stock price movement

This project successfully combines multiple technical domains (web development, data science, NLP, financial APIs) into one impressive, functional application that any teacher or employer would find engaging and technically sound.