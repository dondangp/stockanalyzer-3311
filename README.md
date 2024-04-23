# stockanalyzer-3311
Try it out: https://stockanalyzer.streamlit.app/

**Vision Statement** - 
Our vision is to revolutionize the way individuals engage with the stocks market by providing an unparalleled, intuitive cryptocurrency analysis experience. We aim to empower investors of all levels with real-time insights, personalized investment strategies, and provide users with specific information that are currently underserved by current stock apps. The app is solely meant to analyze the cryptocurrency market and can be used as an assistant to help users analyze charts. The app has innovative features such as personalized tips, cryptocurrencies’ finances, comparing multiple stocks in one graph, including top 10 trending news about the stock, and more! StockAnalyzer is committed to democratizing stock market analysis, making it accessible and understandable for both novices and seasoned investors.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features: `Stock Comparison, Stock Chart, News, Videos,Articles, Tips` <br/>
`Selecting Stock`: The user can input a stock in the stock ticker input and select a date range. The graph will populate the stock's adjusted close (y-axis) and the date (x-axis). </br>
`Color Wheel`: To promote personalization and usability, we implemented a color wheel feature where users can select a color and update the graph's line color. </br>
`Stock Comparison`: allows users to compare an infinite amount of stocks - yfinance module <br/>
`Stock Chart`: comprehensive financial data; such as cash flow, balance sheet, index chart, and quarterly balance sheet - yfinance module <br/>
`News`: Shows top 10 news of a stock from recent to least recent which also calculates a sentiment value score. - stocknews module <br/>
`Videos`: Scraped stock guide videos from influencers who are trusted in the stock community. - Youtube Data v3 API <br/>
`Articles`: Shows trending news across from all stocks from recent to least recent articles. - Polygon.io API <br/>
`Tips`: Generated tips from a list of quotes from trusted stock influencers.

https://www.alphavantage.co/ - Sign up for a free Alpha Vantage API key <br/>
https://polygon.io/dashboard - Sign up for a free polygon key which gives access to stock endpoints. In this app, we used it for the articles feature.

Create a .streamlit folder and inside .streamlit make a secrets.toml file with the following content:
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


Changes:
We transitioned our stock tracking application's financial data services from Alpha Vantage API to Polygon.io. The primary reason for this change is the need for an API that offers higher request limits and real-time data, essential for enhancing our app's functionality and user experience. Despite Alpha Vantage's benefits, its restrictive daily usage limit of 25 requests has become inadequate for our expanding user base. Polygon.io not only provides a more generous usage policy but also remains cost-effective as it offers free services that meet our current needs. The integration of Polygon.io's API requires careful handling to maintain data accuracy and system stability. We considered continuing with Alpha Vantage; however, its limitations in handling higher data volumes effectively necessitated our switch to a more scalable solution like Polygon.io.
