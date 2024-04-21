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
from math import ceil
import requests

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
    "https://www.youtube.com/watch?v=63oF8BOMMB8&ab_channel=FREENVESTING"
    "https://www.youtube.com/watch?v=Wk-h2CwEH5k&ab_channel=TradingLab",
    "https://www.youtube.com/watch?v=SfLP1CgLP30&ab_channel=NewMoney",
    "https://www.youtube.com/watch?v=pDuIvrirPPc&ab_channel=BobSharpe",
    "https://www.youtube.com/watch?v=lNdOtlpmH5U&ab_channel=AliAbdaal",
    "https://www.youtube.com/watch?v=-ZscZv-IMyI&ab_channel=AliAbdaal",
    "https://www.youtube.com/watch?v=CYG5E8-DUQc&ab_channel=ImanGadzhi",
    "https://www.youtube.com/watch?v=uCjcc1TXk5c&ab_channel=ImanGadzhi",
    "https://www.youtube.com/watch?v=RaKfKl9G-Q4&ab_channel=DayTradingAddict",
    "https://www.youtube.com/watch?v=BWrkByUnfEk&ab_channel=FinTek",
    "https://www.youtube.com/watch?v=wnCQ4ICBIfc&ab_channel=TickerSymbol%3AYOU"
]
video_array = VideoArray(video_urls)
video_array.shuffle_videos()
selected_videos = video_array.get_videos()

def fetch_stock_news(ticker, polygon_key):
        base_url = "https://api.polygon.io/v2/reference/news"
        params = {
            "ticker": ticker,
            "limit": 20,  # Adjust as needed
            "apiKey": polygon_key
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            news_items = response.json().get("results", [])
            return news_items
        else:
            print("Failed to fetch news:", response.text)
            return []
# Load environment variables and retrieve API keys
load_dotenv()
polygon_key = os.getenv('polygon_key')
# Streamlit app setup
# Streamlit app setup
st.markdown("<center><h1 style='color: red;'>StockAnalyzer</h1></center>", unsafe_allow_html=True)
stock = st.sidebar.text_input('Stock', value='AAPL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

# Download stock data
data = yf.download(stock, start=start_date, end=end_date).reset_index()

# Graph style with color picker
graph_style = st.sidebar.radio("Choose Graph Style", ("Default",))
line_color = st.sidebar.color_picker("Choose a line color for the graph", '#00f')

# Display stock price graph
fig = px.line(data, x='Date', y='Adj Close', title=f"{stock} Stock Price")
if graph_style == "Default":
    fig.update_traces(line=dict(color=line_color))
else:
    fig.update_traces(line=dict(dash='dot', color=line_color), marker=dict(size=10, color=line_color))
st.plotly_chart(fig)



# Tabs for different sections of the app
stock_comparison, financialData, news, videos_tab, articles_tab, tips_tab = st.tabs(["Stock Comparison", "Financial Data", "Selected News", "Videos", "Articles", "Tips"])

#financial data implementation
with financialData:
    # Price Index
    st.header('Price Index')
    data2 = data.copy()
    data2['% Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return = data2['% Change'].mean() * 252 * 100
    st.write('Annual Return is ', annual_return, '%')
    stdev = np.std(data2['% Change']) * np.sqrt(252)
    st.write('Standard Deviation is ', stdev * 100, '%')
    st.write('Risk Adj. Return is', annual_return / (stdev * 100))
    st.header(f"{stock} Financials")
    
    # Create a Ticker object for the selected stock
    ticker = yf.Ticker(stock)

    # Fetch and display the balance sheet
    st.subheader("Balance Sheet")
    balance_sheet = ticker.balance_sheet
    st.write(balance_sheet)

    # Fetch and display the quarterly balance sheet
    st.subheader("Quarterly Balance Sheet")
    quarterly_balance_sheet = ticker.quarterly_balance_sheet
    st.write(quarterly_balance_sheet)

    # Fetch and display the cash flow statement
    st.subheader("Cash Flow Statement")
    cashflow = ticker.cashflow
    st.write(cashflow)

   

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
    average_title_sentiment = ceil(total_title_sentiment / 10 * 100) / 100
    average_summary_sentiment = ceil(total_summary_sentiment / 10 * 100) / 100
    
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


    # Implement articles tab
    with articles_tab:
        st.header("Trending Stock Articles")
        
        # Fetch stock news using the function
        news_items = fetch_stock_news(stock, polygon_key)
        
        # Display the news articles
        for item in news_items:
            st.subheader(item["title"])
            st.image(item["image_url"])
            st.write(item["description"])
            st.markdown(f"[Read more]({item['article_url']})")

    # Implement tips tab
    with tips_tab:
        st.write("Consider the following tips before investing in stocks:")
        for tip in selected_tips:
            st.write(f"- {tip}")
