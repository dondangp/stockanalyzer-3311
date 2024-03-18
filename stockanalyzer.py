# Import required libraries
from dotenv import load_dotenv  # To load environment variables from .env file
import os
import streamlit as st  # For creating the web app
import pandas as pd
import numpy as np  # For numerical operations
import yfinance as yf  # For downloading stock data
import plotly.express as px  # For creating interactive plots
from stocknews import StockNews  # For fetching news related to stocks
import random  # For shuffling the tips list
import plotly.graph_objects as go  # For more customized plots
from plotly.subplots import make_subplots  # Importing make_subplots for subplot creation

# Class to hold an array of stock tips for users
class StockTips:
    def __init__(self):
        self.tips = [
            "Always do your own research and due diligence before buying a stock.",
            "Diversify your portfolio to spread risk.",
            "Invest in companies you understand and believe in for the long term.",
            "Avoid making decisions based solely on price movements or market speculation.",
            "Monitor your investments regularly and stay updated with market news.",
            "Consider the company's fundamentals, such as earnings, valuation, and growth potential.",
            "Always be cautious of stocks with extremely high valuations or rapid price increases.",
            "Set a budget and avoid investing money you can't afford to lose.",
            "Consider setting stop-loss orders to limit potential losses.",
            "Stay patient and avoid emotional decision-making."
        ]

    def shuffle_tips(self):
        random.shuffle(self.tips)
    
    def get_tips(self, count=3):
        return self.tips[:count]

class VideoArray:
    def __init__(self, videos):
        self.videos = videos
    
    def shuffle_videos(self):
        random.shuffle(self.videos)
    
    def get_videos(self, count=3):
        return self.videos[:count]

# Initialize stock tips and video arrays
stock_tips = StockTips()
stock_tips.shuffle_tips()
selected_tips = stock_tips.get_tips()

video_urls = [
    "https://www.youtube.com/watch?v=i5OZQQWj5-I&ab_channel=TradingLab",
    "https://www.youtube.com/watch?v=rMMnk6Yvxic&ab_channel=BrianJung",
    "https://www.youtube.com/watch?v=86rPBAnRCHc&ab_channel=BrianJung",
    "https://www.youtube.com/watch?v=8Ij7A1VCB7I&ab_channel=MarkTilbury",
    "https://www.youtube.com/watch?v=bEElvs_5byk&ab_channel=MikiRai"
]
video_array = VideoArray(video_urls)
video_array.shuffle_videos()
selected_videos = video_array.get_videos()

# Load environment variables and retrieve API keys
load_dotenv()
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

# Streamlit app setup
st.markdown("<center><h1 style='color: pink;'>StockAnalyzer</h1></center>", unsafe_allow_html=True)
stock = st.sidebar.text_input('Stock', value='AAPL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')
graph_style = st.sidebar.radio("Choose Graph Style", ("Default", "Changed"))

# Download stock data
data = yf.download(stock, start=start_date, end=end_date).reset_index()

# Display stock price graph
fig = px.line(data, x='Date', y='Adj Close', title=f"{stock} Stock Price")
if graph_style == "Default":
    fig.update_traces(line=dict(color='Pink'))
else:
    fig.update_traces(line=dict(dash='dot', color='blue'), marker=dict(size=10, color='LightSkyBlue'))
st.plotly_chart(fig)

# Tabs for different sections of the app
news, stock_comparison, videos_tab, tips_tab = st.tabs(["News", "Stock Comparison", "Videos", "Tips"])

# Implement tips tab
with tips_tab:
    st.write("Consider the following tips before investing in stocks:")
    for tip in selected_tips:
        st.write(f"- {tip}")

# Implement videos tab
with videos_tab:
    st.header("Educational Videos on Stock Investment")
    for video_url in selected_videos:
        st.video(video_url)

#news    
with news:
    st.header(f'Trending News of {stock}')
    sn = StockNews(stock, save_news=False)
    df_news = sn.read_rss()
    
    # Initialize variables to store the sum of sentiments
    total_title_sentiment = 0
    total_summary_sentiment = 0
    
    for i in range(10):
        st.subheader(f'News {i + 1}')
        st.write(df_news['published'].iloc[i])
        st.write(df_news['title'].iloc[i])
        st.write(df_news['summary'].iloc[i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment: {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment: {news_sentiment}')
        
        # Accumulate sentiments
        total_title_sentiment += title_sentiment
        total_summary_sentiment += news_sentiment
    
    # Calculate average sentiments
    average_title_sentiment = total_title_sentiment / 10
    average_summary_sentiment = total_summary_sentiment / 10
    
    # Display average sentiments
    st.markdown(f'## Average Title Sentiment: {average_title_sentiment}')
    st.markdown(f'## Average News Sentiment: {average_summary_sentiment}')

    with stock_comparison:
        st.header("Stock Comparison")
        selected_tickers = st.multiselect(
            'Select stocks for comparison',
            ['TSLA', 'AAPL', 'AMZN', 'MSFT', 'GOOGL'],
            default=['TSLA', 'AAPL']
        )

        comparison_data = {}
        for t in selected_tickers:
            comparison_data[t] = yf.download(t, start=start_date, end=end_date)

        comparison_fig = px.line(title='Stock Comparison')
        for t, d in comparison_data.items():
            comparison_fig.add_scatter(x=d.index, y=d['Adj Close'], name=t)
        st.plotly_chart(comparison_fig)

        comparison_metrics = {}
        for t, d in comparison_data.items():
            daily_return = d['Adj Close'] / d['Adj Close'].shift(1) - 1
            annual_return = daily_return.mean() * 252
            stdev = np.std(daily_return) * np.sqrt(252)
            comparison_metrics[t] = {
                'Annual Return': annual_return,
                'Standard Deviation': stdev,
                'Risk Adj. Return': annual_return / stdev
            }

        comparison_df = pd.DataFrame(comparison_metrics).T
        st.table(comparison_df)
