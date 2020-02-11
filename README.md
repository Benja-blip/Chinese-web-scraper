# Chinese-web-scraper

View short video demo here: https://youtu.be/nbtM0ScR6PE

This web scraper is designed to regularly visit the Chinese news aggregator website, Toutiao.com. More specifically, this program does the following:

1) Connect to a proxy server at a random location
2) Visit toutiao.com
3) Search the Chinese word for America, 美国, in the main page's search bar
4) Visit each article in the resulting list of articles containing '美国' in the headline
5) Scrape the text of the article by writing to a dictionary
6) Each dictionary is appended to a list and eventually written to a csv file
- The program manages a total of three different lists of dictionaries, each with varying maximum lengths. These lists are designed to regulate the number and flow of new entries collected with each connection to a proxy server. When one list reaches maximum capacity, all of its contents (text from articles) are either transferred to another list or written to a csv file.
- In particular, the 'intermediary articles' list, while serving no real purpose in the program's current iteration, it could be useful for more complex proxy server procedures.
- Upon successfully scraping a specified number of articles (currently 4, but easiliy changed), all articles are written to a CSV file and the program disconnects from the proxy server.

The potential use of this program could be corpus development, sentiment analysis, or both. Future versions will include segmentation of Chinese text that is collected, along with frequency distributions as well as other features.
