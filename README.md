# Chinese-web-scraper

This web scraper is designed to regularly visit the Chinese news aggregator website, Toutiao.com. More specifically, this program does the following:

1) Connect to a proxy server at a random location
2) Search the Chinese word for America, 美国
3) Visit each article in the resulting list of articles containing '美国' in the headline
4) Scrape the text of the article by writing to a dictionary
- There are three lists of dictionaries, each with varying maximum lengths, mainly to manage the number of new entries collected with each connection to a proxy server. When one list reaches maximum capacity, all of its contents are either transferred to another list or written to a csv file.
- In particular, the 'intermediary articles' list, while serving no real purpose in the program's current iteration, it could be useful for more complex proxy server procedures.
- Upon successfully scraping a specified number of articles (currently 4), all articles are written to a CSV file and the program disconnects from the proxy server.

The potential use of this program could be corpus development, sentiment analysis, or both. Future versions will include segmentation of Chinese text that is collected, along with frequency distributions as well as other features.
