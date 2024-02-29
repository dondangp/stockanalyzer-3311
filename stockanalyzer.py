# Import required libraries
from dotenv import load_dotenv  # To load environment variables from .env file
import os
import streamlit as st  # For creating the web app
import pandas as pd
import numpy as np  # For numerical operations
import yfinance as yf  # For downloading stock data
import plotly.express as px  # For creating interactive plots
from alpha_vantage.fundamentaldata import FundamentalData  # For accessing Alpha Vantage API
from stocknews import StockNews  # For fetching news related to stocks
import random  # For shuffling the tips list
import plotly.graph_objects as go  # For more customized plots
from plotly.subplots import make_subplots  # Importing make_subplots for subplot creation

# Class to hold an array of stock tips for users
class StockTips:
    def __init__(self):
        # Initialize the tips array within the class
        self.tips = [
            "Always do your own research and due diligence before buying a stock.",
            "Diversify your portfolio to spread risk.",
            "Invest in companies you understand and believe in for the long term.",
            "Avoid making decisions based solely on price movements or market speculation.",
            "Monitor your investments regularly and stay updated with market news.",
            "Consider the company's fundamentals, such as earnings, val~uation, and growth potential.",
            "Always be cautious of stocks with extremely high valuations or rapid price increases.",
            "Set a budget and avoid investing money you can't afford to lose.",
            "Consider setting stop-loss orders to limit potential losses.",
            "Stay patient and avoid emotional decision-making."
        ]

    
    def shuffle_tips(self):
        # Shuffle the tips array
        random.shuffle(self.tips)
    
    def get_tips(self, count=3):
        # Return the first `count` number of tips
        return self.tips[:count]

#Hold an array of video tips
class VideoArray:
    def __init__(self):
        self.videos = []
stock_tips = StockTips()  # Create an instance of StockTips
stock_tips.shuffle_tips()  # Shuffle the tips
selected_tips = stock_tips.get_tips()  # Get 3 shuffled tips

# Display the selected tips
for tip in selected_tips:
    print(f"- {tip}")

# Load environment variables
load_dotenv()

# Retrieve API keys from .env file
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

# Centered title
st.markdown("<center><h1 style='color: pink;'>StockAnalyzer</h1></center>", unsafe_allow_html=True)

# Sidebar inputs for selecting stock and date range
stock = st.sidebar.text_input('stock', value='AAPL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Download stock data using yfinance
data = yf.download(stock, start=start_date, end=end_date).reset_index()

# Initialize a variable to hold the graph style and create conditional logic for styling
graph_style = st.sidebar.radio("Choose Graph Style", ("Default", "Changed"))
if graph_style == "Default":
    fig = px.line(data, x='Date', y='Adj Close', title=f"{stock} Stock Price")
    fig.update_traces(line=dict(color='Pink'))
else:
    fig = px.line(data, x='Date', y='Adj Close', title=f"{stock} Stock Price")
    fig.update_traces(line=dict(dash='dot', color='blue'), marker=dict(size=10, color='LightSkyBlue'))

# Display the graph
st.plotly_chart(fig)

# Tabs for different sections of the app: News and Tips
news, tips_tab, videos = st.tabs(["News", "Tips", "Videos"])

# Tips tab content
with tips_tab:
    st.write("Consider the following tips before investing in stocks:")
    for tip in selected_tips:
        st.write(f"- {tip}")


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
    with videos:
        st.header(f'Video Education')
        video_url = 'https://www.youtube.com/watch?v=-LbKXPoz7-A&ab_channel=%ED%94%BD%ED%8A%B8PickStream'
        st.video(video_url)
