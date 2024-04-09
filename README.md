# stockanalyzer-3311
Our vision is to revolutionize the way individuals engage with the stocks market by providing an unparalleled, intuitive cryptocurrency analysis experience. We aim to empower investors of all levels with real-time insights, personalized investment strategies, and provide users with specific information that are currently underserved by current stock apps. The app is solely meant to analyze the cryptocurrency market and can be used as an assistant to help users analyze charts. The app has innovative features such as personalized tips, cryptocurrencies’ finances, comparing multiple stocks in one graph, including top 10 trending news about the stock, and more! StockAnalyzer is committed to democratizing stock market analysis, making it accessible and understandable for both novices and seasoned investors.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features: `Stock Comparison, Stock Chart, News, Videos,Articles, Tips`
`Stock Comparison`: allows users to compare an infinite amount of stocks - yfinance module
`Stock Chart`: comprehensive financial data; such as cash flow, balance sheet, index chart, and quarterly balance sheet - yfinance module
`News`: Shows top 10 news of a stock from recent to least recent which also calculates a sentiment value score. - stocknews module
`Videos`: Scraped stock guide videos from influencers who are trusted in the stock community. - Youtube Data v3 API
`Articles`: Shows trending news across from all stocks from recent to least recent articles. - Polygon.io API 
`Tips`: Generated tips from a list of quotes from trusted stock influencers.

https://www.alphavantage.co/ - Sign up for a free Alpha Vantage API key <br/>
https://polygon.io/dashboard - Sign up for a free polygon key which gives access to stock endpoints. In this app, we used it for the articles feature.

Create a .env file with the following content:<br/>
ALPHA_VANTAGE_KEY =  ``(This is where you put your free/paid key)`` <br/>
polygon_key = ``(This is where you put your free/paid key)``

How to run:
**pip3 install:**
numpy,
pandas,
plotly,
python-dotenv,
stocknews,
streamlit,
yfinance

OR import modules via requirements.txt using this command:``pip install -r requirements.txt``

To run the program run this in the command line:
``streamlit run stockanalyzer.py``
