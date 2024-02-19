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

# Created an array with tips for users
TIPS_BEFORE_BUYING = [
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

random.shuffle(TIPS_BEFORE_BUYING)  # Shuffle the array to display tips
selected_tips = TIPS_BEFORE_BUYING[:3]

# Load environment variables
load_dotenv()

# Retrieve API keys from .env file
alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')

# Streamlit app
st.title('StockAnalyzer')

# Sidebar inputs
stock = st.sidebar.text_input('stock', value='AAPL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Download stock data
data = yf.download(stock, start=start_date, end=end_date).reset_index()

# Initialize a variable to hold the graph style
graph_style = st.sidebar.radio("Choose Graph Style", ("Default", "Changed"))

# Conditional logic based on the selected graph style
if graph_style == "Default":
    fig = px.line(data, x='Date', y='Adj Close', title=stock)
    fig.update_traces(line=dict(color='Pink'))
else:
    fig = px.line(data, x='Date', y='Adj Close', title=stock)
    fig.update_traces(line=dict(dash='dot', color='blue'), marker=dict(size=10, color='LightSkyBlue'))

st.plotly_chart(fig)



# Tabs for different sections of the app: News, Price Movement, and Tips
news, pricing_movement, tips_tab = st.tabs(["News", "Price Movement", "Tips"])

# Tips tab content
with tips_tab:
    st.write("Consider the following tips before investing in stocks:")
    for tip in selected_tips:
        st.write(f"- {tip}")

# Pricing Data tab content
with pricing_movement:
    st.header(f'Price Movements and Volume for {stock}')

    # Calculate the percentage change of the stock's adjusted close price for the table
    data['% Change'] = data['Adj Close'].pct_change()
    # Prepare the table data
    table_data = data[['Date', 'Adj Close', '% Change']].copy()
    table_data.dropna(inplace=True)  # Drop the first row where % change is NaN due to no previous day comparison

    # Display the dataframe with percentage changes
    st.write("Price Movements and Percentage Changes:")
    st.dataframe(table_data.style.format({"% Change": "{:.2%}"}), height=300)

    # Calculate Moving Averages for the graph
    data['50_MA'] = data['Adj Close'].rolling(window=50).mean()
    data['200_MA'] = data['Adj Close'].rolling(window=200).mean()

    # Create Plotly subplots for the graph
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=(f'{stock} Price Movement', 'Volume'), row_width=[0.2, 0.7])

    # Price and Moving Averages
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Adj Close'], name='Adj Close', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['50_MA'], name='50-Day MA', line=dict(color='orange', dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data['Date'], y=data['200_MA'], name='200-Day MA', line=dict(color='green', dash='dot')), row=1, col=1)

    # Volume
    fig.add_trace(go.Bar(x=data['Date'], y=data['Volume'], name='Volume', marker_color='lightblue'), row=2, col=1)

    # Update y-axis titles and layout
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_layout(height=600, title=f'{stock} Stock Data Analysis', xaxis_title="Date")

    # Display the plot
    st.plotly_chart(fig)

    # Calculate and display annual return, standard deviation, and risk-adjusted return
    annual_return = table_data['% Change'].mean() * 252
    stdev = table_data['% Change'].std() * np.sqrt(252)
    risk_adjusted_return = annual_return / stdev

    # Metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Annual Return", value=f"{annual_return * 100:.2f}%")
    with col2:
        st.metric(label="Standard Deviation", value=f"{stdev * 100:.2f}%")
    with col3:
        st.metric(label="Risk Adjusted Return", value=f"{risk_adjusted_return:.2f}")




# Top 10 News tab content
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


