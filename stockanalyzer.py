# Import required libraries
from dotenv import load_dotenv  # To load environment variables from .env file
from alpha_vantage.fundamentaldata import FundamentalData  # For accessing Alpha Vantage API
import plotly.express as px  # For creating interactive plots
import streamlit as st  # For creating the web app
import yfinance as yf  # For downloading stock data
from stocknews import StockNews  # For fetching news related to stocks
import random  # For shuffling the tips list
import os  # For accessing environment variables from the operating system
import numpy as np  # For numerical operations

# Created an array with tips for users
TIPS_BEFORE_BUYING = [
    "Develop a trading plan with clear goals, risk tolerance, and strategies.",
    "Understand technical analysis to identify buying and selling opportunities.",
    "Stay informed about market trends and news that could impact stock prices.",
    "Use stop-loss and take-profit orders to manage risk and protect gains.",
    "Practice paper trading to test strategies without financial risk.",
    "Limit your exposure by not putting all your capital in a single trade.",
    "Be mindful of trading fees and taxes, as they can eat into your profits.",
    "Learn from your trades by keeping a journal of your decisions and outcomes.",
    "Stay disciplined and don't let emotions drive your trading decisions.",
    "Continuously educate yourself on market conditions and trading techniques."
]

# Shuffle the array to display tips
random.shuffle(TIPS_BEFORE_BUYING)

# Display only three tips at a time
selected_tips = TIPS_BEFORE_BUYING[:3] 

# Load environment variables
load_dotenv()

# Retrieve API keys from .env file
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

# Initialize the Streamlit app
st.markdown("<h1 style='text-align: center;'>StockAnalyzer</h1>", unsafe_allow_html=True)

# Sidebar inputs for user to select stock ticker, start, and end date
ticker = st.sidebar.text_input('Stock', value='AAPL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Download stock data using yfinance library
data = yf.download(ticker, start=start_date, end=end_date).reset_index()

# Create a line plot of the stock data using Plotly Express
fig = px.line(data, x='Date', y='Adj Close', title=f'{ticker} Stock Price')
# Add markers to the line plot for better visualization
fig.update_traces(line=dict(color='Pink'), marker=dict(size=7, color='LightSkyBlue'))
# Update y-axis title to "Price"
fig.update_yaxes(title_text='Price')
# Display the plot in the Streamlit app
st.plotly_chart(fig)

# Tabs for different sections of the app: News, Price Movement, and Tips
news, pricing_data, tips_tab = st.tabs(["News", "Price Movement", "Tips"])

# Tips tab content
with tips_tab:
    st.write("Consider the following tips before investing in stocks:")
    for tip in selected_tips:
        st.write(f"- {tip}")

# Pricing Data tab content
with pricing_data:
    st.header('Price Movements')
    # Calculate the percentage change of the stock's adjusted close price
    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    # Display the dataframe with percentage changes
    st.dataframe(data2.style.format({"% Change": "{:.2%}"}), height=300)
    # Calculate and display annual return, standard deviation, and risk-adjusted return
    annual_return = data2['% Change'].mean() * 252
    stdev = data2['% Change'].std() * np.sqrt(252)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Annual Return", value=f"{annual_return * 100:.2f}%")
    with col2:
        st.metric(label="Standard Deviation", value=f"{stdev * 100:.2f}%")
    with col3:
        st.metric(label="Risk Adjusted Return", value=f"{annual_return / stdev:.2f}")

# Top 10 News tab content
with news:
    st.header(f'News of {ticker}')
    # Fetch and display the top 10 news related to the selected stock
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(min(10, len(df_news))):
        st.subheader(f'News {i + 1}')
        st.write(df_news['published'].iloc[i])
        st.write(df_news['title'].iloc[i])
        st.write(df_news['summary'].iloc[i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment: {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment: {news_sentiment}')
