from datetime import timedelta
from flask import render_template, make_response, request, current_app
from app import app
from functools import update_wrapper
from yahoo_finance import Share

import os

def crossdomain(origin=None, methods=None, headers=None,
              max_age=21600, attach_to_all=True,
              automatic_options=True):
  if methods is not None:
      methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
      headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
      origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
      max_age = max_age.total_seconds()

  def get_methods():
      if methods is not None:
          return methods

      options_resp = current_app.make_default_options_response()
      return options_resp.headers['allow']

  def decorator(f):
      def wrapped_function(*args, **kwargs):
          if automatic_options and request.method == 'OPTIONS':
              resp = current_app.make_default_options_response()
          else:
              resp = make_response(f(*args, **kwargs))
          if not attach_to_all and request.method != 'OPTIONS':
              return resp

          h = resp.headers
          h['Access-Control-Allow-Origin'] = origin
          h['Access-Control-Allow-Methods'] = get_methods()
          h['Access-Control-Max-Age'] = str(max_age)
          h['Access-Control-Allow-Credentials'] = 'true'
          h['Access-Control-Allow-Headers'] = \
              "Origin, X-Requested-With, Content-Type, Accept, Authorization"
          if headers is not None:
              h['Access-Control-Allow-Headers'] = headers
          return resp

      f.provide_automatic_options = False
      return update_wrapper(wrapped_function, f)
  return decorator

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html")

@app.route('/technical')
def technical():
  return render_template("technical.html",
                         title='Technical Analysis')

@app.route("/technical/query/<stock_code>/<start_time>/<end_time>", methods=['POST'])
@crossdomain(origin='*')
def technical_query(stock_code, start_time, end_time):
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

  historical_data = stock.get_historical(start_time, end_time)

  print('historical_data')
  print(historical_data)



  data_text = "date\t" + "High\t" + "Low\n"
  # data_text = "date\t" + "High\t" + "Low\t" + "Open\t" + "Close\t"

  for index, value in enumerate(historical_data):
    date = str(historical_data[len(historical_data) - 1 - index]['Date'])
    date = date.replace('-','')
    stock_high = str(historical_data[len(historical_data) - 1 - index]['High'])
    stock_low = str(historical_data[len(historical_data) - 1 - index]['Low'])
    # stock_open = str(historical_data[len(historical_data) - 1 - index]['Open'])
    # stock_close = str(historical_data[len(historical_data) - 1 - index]['Close'])
    data_text += date + "\t" + stock_high + "\t" + stock_low + "\n"
    # data_text += date + "\t" + stock_high + "\t" + stock_low + "\n" + stock_open + "\t" + stock_close + "\n"

  current_directory = os.getcwd()
  data_directory = current_directory + '/data/highlow.tsv'
  data = open(data_directory, 'w')

  data.write(data_text)
  
  data.close()

  data_text = "date\t" + "Open\t" + "Close\n"

  for index, value in enumerate(historical_data):
    date = str(historical_data[len(historical_data) - 1 - index]['Date'])
    date = date.replace('-','')
    stock_open = str(historical_data[len(historical_data) - 1 - index]['Open'])
    stock_close = str(historical_data[len(historical_data) - 1 - index]['Close'])
    data_text += date + "\t" + stock_open + "\t" + stock_close + "\n"

  current_directory = os.getcwd()
  data_directory = current_directory + '/data/openclose.tsv'
  data = open(data_directory, 'w')

  data.write(data_text)
  
  data.close()

  return render_template("technical.html",
                         title='Technical Analysis',
                         technical=True,
                         data=True)

@app.route("/technical/clear", methods=['POST'])
@crossdomain(origin='*')
def technical_clear():
  data_text = "date\tNIL\n"

  current_directory = os.getcwd()
  data_directory = current_directory + '/data/technical.tsv'
  data = open(data_directory, 'w')

  data.write(data_text)
  
  data.close()

  return render_template("technical.html",
                         title='Technical Analysis',
                         technical=True,
                         data=True)

@app.route("/technical/data/<file_name>")
@crossdomain(origin='*')
def technical_data(file_name):
  current_directory = os.getcwd()
  data_directory = current_directory + '/data/' + file_name + '.tsv'
  data = open(data_directory, 'r')
  return data.read()

@app.route('/social')
def social():
  return render_template("social.html",
                         title='Social Analysis')

@app.route("/social/clear", methods=['POST'])
@crossdomain(origin='*')
def social_clear():
  data_text = '{"name": "sentiment","children": []}'

  current_directory = os.getcwd()
  data_directory = current_directory + '/data/social.json'
  data = open(data_directory, 'w')

  data.write(data_text)
  
  data.close()

  return render_template("social.html",
                         title='Social Analysis',
                         data=True)

@app.route("/social/data")
def social_data():
  current_directory = os.getcwd()
  data_directory = current_directory + '/data/social.json'
  data = open(data_directory, 'r')
  return data.read()