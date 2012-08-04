System overview
---------------
Stock market analysis toolit is written for purpose of automatically stock market analysis, especially for Chinese markdet.

This system can crawl stock market data, visualize them. By simulating and comparing to the history data, automatic trading system can test their strategy to find if it can earn profit in the history.


Struture of this system
-----------------------
This system is seperated into three main components.

- Stock market data crawler
- Visualize toolkit to show history data
- Simulation system for strategy simulation

To know the meaning of each file, take Filelist.md for reference.

Stock market data crawler
-------------------------
There are many stock trading data available in the internet.

The most popular two of these are  
- Yahoo finance
- Google finance

There are many toolkits and code snippet for accessing those data, but there is no official sdk yet. The most poplular financial project in my knowledge in [ultrafinance](code.google.com/p/ultrafinance).

In this project, I use the trading data of Shenzhen market and Shanghai market. In the early development, some dumped data of Dow Jones was also used.

The company list of shenzhen market is downloaded from the official site of Shenzhen market, and translated from xsl into the form that can be used by python code.





