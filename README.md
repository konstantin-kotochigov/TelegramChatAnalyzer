# TelegramChatAnalyzer

Script for basic text analytics of telegram text data

Steps:
- Export chat data in HTML format via Telegram desktop app (alternative - ues 3rd party tools to export right into DB)
- Parse chunks of data using BeautifulSoup python library
- Load it into Pandas dataframe
- Preocess data and do some text analytics using Sklearn and bigARTM
