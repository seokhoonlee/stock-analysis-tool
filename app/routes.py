from datetime import timedelta
from flask import render_template, make_response, request, current_app
from app import app
from functools import update_wrapper

import file_manager

import os

"""avoid crossdomain"""
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

"""simeple page routing"""
@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html")

@app.route('/technical')
def technical():
  return render_template("technical.html",
                         title='Technical Analysis')

@app.route('/social')
def social():
  return render_template("social.html",
                         title='Social Analysis')

"""query routing"""
@app.route("/technical/query/<stock_code>/<start_time>/<end_time>", methods=['POST'])
@crossdomain(origin='*')
def technical_query(stock_code, start_time, end_time):
  file_manager.write_technical_files(stock_code, start_time, end_time)

  return render_template("technical.html",
                         title='Technical Analysis',
                         technical=True,
                         data=True)

@app.route("/social/query/<key_word>", methods=['POST'])
@crossdomain(origin='*')
def social_query(key_word):
  file_manager.write_social_files(key_word)

  return render_template("social.html",
                         title='Social Analysis',
                         technical=True,
                         data=True)

"""clear routing"""
@app.route("/technical/clear", methods=['POST'])
@crossdomain(origin='*')
def technical_clear():
  file_manager.clear_technical_files()

  return render_template("technical.html",
                         title='Technical Analysis',
                         technical=True,
                         data=True,
                         clear=True)

@app.route("/social/clear", methods=['POST'])
@crossdomain(origin='*')
def social_clear():
  file_manager.clear_social_files()

  return render_template("social.html",
                         title='Social Analysis',
                         data=True)

"""data read routing"""
@app.route("/technical/data/<file_name>")
@crossdomain(origin='*')
def technical_data(file_name):
  extension = '.tsv'

  return file_manager.read_from_file(file_name, extension)

@app.route("/social/data")
@crossdomain(origin='*')
def social_data():
  file_name = 'social'
  extension = '.json'

  return file_manager.read_from_file(file_name, extension)