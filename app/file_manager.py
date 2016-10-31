import os
import quandl
import tweepy

auth = tweepy.OAuthHandler('ZnSb3IMNZXb7gmQtwGne1M5Mn', 'HnIuFSbFpgpMytffuxjViQOJmEpxT8WSPermMsyU9ul8OpOMSi')
auth.set_access_token('793012381852897281-VCldOuLSsn8CLiAxl1IbYERKkoExdZL', 'cTRKEpnFaMuRNkf4zWr6ePwD95mJVjbCm1bNv5eu2xGjL')

api = tweepy.API(auth)

from yahoo_finance import Share

quandl.ApiConfig.api_key = 'VmCnUrM6WssTsDacrM1F'

def write_to_file(directory, data_text):
  current_directory = os.getcwd()
  data_directory = current_directory + directory

  data_file = open(data_directory, 'w')

  data_file.write(data_text)
  
  data_file.close()

def read_from_file(file_name, extension):
  current_directory = os.getcwd()
  data_directory = current_directory + '/data/' + file_name + extension
  data = open(data_directory, 'r')

  return data.read()

def write_technical_files(stock_code, start_time, end_time):
  # """ Experiment on quandl """
  # print('quandl data')
  # mydata = quandl.get("FRED/GDP")
  # print(mydata)
  # print('hello')

  # data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")
  # print(data)

  stock = Share(stock_code)

  print('stock.get_info()')
  print(stock.get_info())

  print('get_price()')
  print(stock.get_price())

  print('get_change()')
  print(stock.get_change())

  print('get_stock_exchange()')
  print(stock.get_stock_exchange())

  print('get_market_cap()')
  print(stock.get_market_cap())

  print('get_book_value()')
  print(stock.get_book_value())

  print('get_ebitda()')
  print(stock.get_ebitda())

  print('get_dividend_share()')  
  print(stock.get_dividend_share())

  print('get_dividend_yield()')
  print(stock.get_dividend_yield())

  print('get_earnings_share()')
  print(stock.get_earnings_share())

  print('get_50day_moving_avg()')
  print(stock.get_50day_moving_avg())

  print('get_200day_moving_avg()')
  print(stock.get_200day_moving_avg())

  print('get_price_earnings_ratio()')
  print(stock.get_price_earnings_ratio())

  print('get_price_earnings_growth_ratio()')
  print(stock.get_price_earnings_growth_ratio())

  print('get_price_sales()')
  print(stock.get_price_sales())

  print('get_price_book()')
  print(stock.get_price_book())

  print('get_short_ratio()')
  print(stock.get_short_ratio())

  print('historical_data')
  print(stock.get_historical(start_time, end_time))

  historical_data = stock.get_historical(start_time, end_time)

  info_text = "Symbol\t" + "Stock Exchange\t" + "Price\t" + "Market Cap\t" + "Book Value\t" + "EBITDA\t" + "50d Moving Avg\t" + "100d Moving Avg\n"
  info_text += str(stock.get_info()['symbol']) + "\t" + str(stock.get_stock_exchange()) + "\t" + str(stock.get_price()) + "\t" + str(stock.get_market_cap()) + "\t" + str(stock.get_book_value()) + "\t";
  info_text += str(stock.get_ebitda()) + "\t" + str(stock.get_50day_moving_avg()) + "\t" + str(stock.get_200day_moving_avg()) + "\n";

  info_directory = '/data/info.tsv'

  write_to_file(info_directory, info_text)

  high_low_text = "date\t" + "High\t" + "Low\n"
  open_close_text = "date\t" + "Open\t" + "Close\n"
  volume_text = "date\t" + "Volume\n"

  for index, value in enumerate(historical_data):
    date = str(historical_data[len(historical_data) - 1 - index]['Date'])
    date = date.replace('-','')

    stock_high = str(historical_data[len(historical_data) - 1 - index]['High'])
    stock_low = str(historical_data[len(historical_data) - 1 - index]['Low'])

    stock_open = str(historical_data[len(historical_data) - 1 - index]['Open'])
    stock_close = str(historical_data[len(historical_data) - 1 - index]['Close'])

    stock_volume = str(int(historical_data[len(historical_data) - 1 - index]['Volume']) / 1000)

    high_low_text += date + "\t" + stock_high + "\t" + stock_low + "\n"
    open_close_text += date + "\t" + stock_open + "\t" + stock_close + "\n"
    volume_text += date + "\t" + stock_volume + "\n"

  high_low_directory = '/data/highlow.tsv'
  open_close_directory = '/data/openclose.tsv'
  volume_directory = '/data/volume.tsv'

  write_to_file(high_low_directory, high_low_text)
  write_to_file(open_close_directory, open_close_text)
  write_to_file(volume_directory, volume_text)

  ratio_text = "name\t" + "value\n"

  if stock.get_change() != None:
    name = "Change"
    value = str(stock.get_change())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_dividend_share() != None:
    name = "Dividend Share"
    value = str(stock.get_dividend_share())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_dividend_yield() != None:
    name = "Divident Yield"
    value = str(stock.get_dividend_yield())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_earnings_share() != None:
    name = "Earning Share"
    value = str(stock.get_earnings_share())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_price_earnings_ratio() != None:
    name = "Price Earning"
    value = str(stock.get_price_earnings_ratio())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_price_earnings_growth_ratio() != None:
    name = "Price Earning Growth"
    value = str(stock.get_price_earnings_growth_ratio())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_price_sales() != None:
    name = "Price Sales"
    value = str(stock.get_price_sales())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_price_book() != None:
    name = "Price Book"
    value = str(stock.get_price_book())
    ratio_text += name + "\t" + value + "\n"

  if stock.get_short_ratio() != None:
    name = "Short"
    value = str(stock.get_short_ratio())
    ratio_text += name + "\t" + value + "\n"

  ratio_directory = '/data/ratio.tsv'

  write_to_file(ratio_directory, ratio_text)

def write_social_files(key_word):
  print key_word

  key_word += ' filter:safe -filter:links' # filter safe tweets without links

  max_tweets = 100 # maximum 100 tweets

  tweets = tweepy.Cursor(api.search, q=key_word, lang='en').items(max_tweets)    

  for tweet in tweets:
    print tweet.text

  return

def clear_technical_files():
  clear_text = "date\tNIL\n"

  high_low_directory = '/data/highlow.tsv'
  open_close_directory = '/data/openclose.tsv'
  volume_directory = '/data/volume.tsv'

  info_directory = '/data/info.tsv'
  ratio_directory = '/data/ratio.tsv'

  write_to_file(high_low_directory, clear_text)
  write_to_file(open_close_directory, clear_text)
  write_to_file(volume_directory, clear_text)

  clear_text = ""

  write_to_file(info_directory, clear_text)
  write_to_file(ratio_directory, clear_text)

def clear_social_files():
  clear_text = '{"name": "sentiment","children": []}'

  social_directory = '/data/social.json'

  write_to_file(social_directory, clear_text)

