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

@app.route('/stockprice')
def stockprice():
  return render_template("stockprice.html",
                         title='Stock Price')

@app.route("/stockprice/query/<stock_code>/<start_time>/<end_time>", methods=['POST'])
@crossdomain(origin='*')
def stockprice_query(stock_code, start_time, end_time):
	stock = Share(stock_code)

	historical_data = stock.get_historical(start_time, end_time)

	data_text = "date\t" + str(stock_code) + "\n"

	for index, value in enumerate(historical_data):
		date = str(historical_data[len(historical_data) - 1 - index]['Date'])
		date = date.replace('-','')
		close = str(historical_data[len(historical_data) - 1 - index]['Close'])
		data_text += date + "\t" + close + "\n"

	current_directory = os.getcwd()
	data_directory = current_directory + '/data/technical.tsv'
	data = open(data_directory, 'w')

	data.write(data_text)
	
	data.close()

	return render_template("stockprice.html",
                         title='Stock Price',
                         stockprice=True,
                         data=True)

@app.route("/stockprice/clear", methods=['POST'])
@crossdomain(origin='*')
def stockprice_clear():
	data_text = "date\tNIL\n"

	current_directory = os.getcwd()
	data_directory = current_directory + '/data/technical.tsv'
	data = open(data_directory, 'w')

	data.write(data_text)
	
	data.close()

	return render_template("stockprice.html",
                         title='Stock Price',
                         stockprice=True,
                         data=True)

@app.route("/stockprice/data")
def stockprice_data():
	current_directory = os.getcwd()
	data_directory = current_directory + '/data/technical.tsv'
	data = open(data_directory, 'r')
	return data.read()

@app.route('/sentiment')
def sentiment():
  return render_template("sentiment.html",
                         title='Market Sentiment')

@app.route("/stockprice/clear", methods=['POST'])
@crossdomain(origin='*')
def sentiment_clear():
	data_text = '{"name": "sentiment","children": []}'

	current_directory = os.getcwd()
	data_directory = current_directory + '/data/social.json'
	data = open(data_directory, 'w')

	data.write(data_text)
	
	data.close()

	return render_template("stockprice.html",
                         title='Stock Price',
                         stockprice=True,
                         data=True)

@app.route("/sentiment/data")
def sentiment_data():
	current_directory = os.getcwd()
	data_directory = current_directory + '/data/social.json'
	data = open(data_directory, 'r')
	return data.read()