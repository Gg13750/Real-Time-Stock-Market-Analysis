import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
from dateutil import parser

# NewsAPI Key
NEWSAPI_KEY = "YOUR_NEWSAPI_KEY"  # <-- Replace with your NewsAPI key

# Set page configuration
st.set_page_config(page_title="Real-Time Stock Sentiment Analysis", page_icon="📈", layout="wide")
st.title("📈 Real-Time Stock Market Sentiment Analysis")
st.markdown("---")

# Sidebar for stock selection
st.sidebar.header("Stock Configuration")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, GOOGL, TSLA)", value="AAPL")
analysis_period = st.sidebar.selectbox("Analysis Period", ["1mo", "5d", "3mo", "6mo"])

@st.cache_data(ttl=300)
def get_stock_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except:
        return None, None

@st.cache_data(ttl=300)
def get_news_headlines(symbol):
    headlines = []
    url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=publishedAt&language=en&apiKey={NEWSAPI_KEY}"
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        for article in articles[:10]:
            # Parse NewsAPI time string to datetime
            try:
                pub_dt = parser.parse(article.get('publishedAt', ''))
                pub_str = pub_dt.strftime("%Y-%m-%d %H:%M")
            except:
                pub_str = ""
            headlines.append({
                'title': article.get('title', ''),
                'summary': article.get('description', ''),
                'published': pub_str,
                'source': article.get('source', {}).get('name', 'Unknown')
            })
    except Exception as e:
        print("NewsAPI fetch failed:", e)

    # Fallback to yfinance if no news from NewsAPI
    if not headlines:
        try:
            stock = yf.Ticker(symbol)
            news = stock.news
            for article in news[:10]:
                pub_time = article.get('providerPublishTime', 0)
                try:
                    pub_str = datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M")
                except:
                    pub_str = ""
                headlines.append({
                    'title': article.get('title', ''),
                    'summary': article.get('summary', ''),
                    'published': pub_str,
                    'source': article.get('publisher', 'Unknown')
                })
        except:
            pass

    return headlines

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        sentiment = "Positive"
        color = "green"
    elif polarity < -0.1:
        sentiment = "Negative"
        color = "red"
    else:
        sentiment = "Neutral"
        color = "gray"
    return {
        'sentiment': sentiment,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'color': color
    }

def create_sentiment_gauge(sentiment_score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = sentiment_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Sentiment Score"},
        delta = {'reference': 0},
        gauge = {
            'axis': {'range': [-100, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [-100, -20], 'color': "red"},
                {'range': [-20, 20], 'color': "yellow"},
                {'range': [20, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

# Main application logic
if stock_symbol:
    with st.spinner(f"Fetching data for {stock_symbol}..."):
        hist_data, stock_info = get_stock_data(stock_symbol, analysis_period)
        news_data = get_news_headlines(stock_symbol)

    if hist_data is None or hist_data.empty:
        st.error(f"Could not fetch data for {stock_symbol}. Please check the stock symbol or try a different analysis period.")
        st.write("Raw data received:", hist_data)
    else:
        col1, col2, col3 = st.columns(3)
        current_price = hist_data['Close'].iloc[-1]
        prev_close = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
        price_change = current_price - prev_close
        price_change_pct = (price_change / prev_close) * 100
        with col1:
            st.metric(label=f"{stock_symbol} Stock Price", value=f"${current_price:.2f}", delta=f"{price_change:.2f} ({price_change_pct:.2f}%)")
        with col2:
            if stock_info:
                market_cap = stock_info.get('marketCap', 'N/A')
                if isinstance(market_cap, (int, float)):
                    market_cap = f"${market_cap / 1e9:.2f}B"
                st.metric(label="Market Cap", value=market_cap)
        with col3:
            volume = hist_data['Volume'].iloc[-1]
            st.metric(label="Volume", value=f"{volume:,.0f}")
        st.subheader("📊 Stock Price Chart")
        fig_price = px.line(hist_data.reset_index(), x='Date', y='Close', title=f"{stock_symbol} Stock Price Over Time")
        fig_price.update_traces(line_color='blue', line_width=2)
        fig_price.update_layout(height=400)
        st.plotly_chart(fig_price, use_container_width=True)

        # News sentiment analysis with fallback logic
        if not news_data or all(n['title'] == '' for n in news_data):
            st.warning("No news headlines could be fetched for sentiment analysis. Try changing the stock symbol or check your internet connection.")
        else:
            st.subheader("📰 News Sentiment Analysis")
            sentiments = []
            news_display = []
            for article in news_data:
                text_to_analyze = f"{article['title']} {article['summary']}"
                sentiment_result = analyze_sentiment(text_to_analyze)
                sentiments.append(sentiment_result)
                news_display.append({
                    'Title': article['title'][:100] + "..." if len(article['title']) > 100 else article['title'],
                    'Sentiment': sentiment_result['sentiment'],
                    'Score': f"{sentiment_result['polarity']:.3f}",
                    'Source': article['source'],
                    'Published': article['published']
                })
            avg_polarity = np.mean([s['polarity'] for s in sentiments])
            avg_subjectivity = np.mean([s['subjectivity'] for s in sentiments])
            col1, col2 = st.columns([1, 2])
            with col1:
                st.plotly_chart(create_sentiment_gauge(avg_polarity), use_container_width=True)
            with col2:
                sentiment_counts = pd.DataFrame(sentiments)['sentiment'].value_counts()
                fig_pie = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, title="Sentiment Distribution",
                                 color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'})
                fig_pie.update_layout(height=300)
                st.plotly_chart(fig_pie, use_container_width=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Sentiment", "Positive" if avg_polarity > 0.1 else "Negative" if avg_polarity < -0.1 else "Neutral")
            with col2:
                st.metric("Sentiment Score", f"{avg_polarity:.3f}")
            with col3:
                st.metric("Subjectivity", f"{avg_subjectivity:.3f}")
            st.subheader("📋 Recent News Headlines")
            news_df = pd.DataFrame(news_display)
            st.dataframe(news_df, use_container_width=True)
            st.subheader("📈 Sentiment Timeline")
            timeline_data = []
            for i, (article, sentiment) in enumerate(zip(news_data, sentiments)):
                timeline_data.append({
                    'Time': article['published'],
                    'Sentiment_Score': sentiment['polarity'],
                    'Article_Number': i + 1
                })
            timeline_df = pd.DataFrame(timeline_data)
            fig_timeline = px.scatter(timeline_df, x='Time', y='Sentiment_Score', title="News Sentiment Over Time", hover_data=['Article_Number'])
            fig_timeline.add_hline(y=0, line_dash="dash", line_color="gray")
            fig_timeline.update_layout(height=400)
            st.plotly_chart(fig_timeline, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Note:** This analysis uses TextBlob for sentiment analysis and Yahoo Finance for stock data. 
Sentiment analysis results should be used as supplementary information and not as the sole basis for investment decisions.
""")
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
