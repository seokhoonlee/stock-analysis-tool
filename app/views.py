from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html")

@app.route('/stockprice')
def stockprice():
  return render_template("stockprice.html",
                         title='Stock Price',
                         stockprice=True)