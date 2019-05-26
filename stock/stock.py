import requests
import datetime as dt
import json
from flask import Flask ,request ,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'

db =SQLAlchemy(app)

stock_url ='https://api.worldtradingdata.com/api/v1/stock?symbol={}&api_token=FZKP0jcyRUsVimi1RSuTQJT4VFy1RmhxyIb5OrCZiWJE8oZA0SSkkWtWgg1w'
intra_day ='https://intraday.worldtradingdata.com/api/v1/intraday?symbol={}&range=1&interval=1&api_token=FZKP0jcyRUsVimi1RSuTQJT4VFy1RmhxyIb5OrCZiWJE8oZA0SSkkWtWgg1w'

class Stock(db.Model):
    id =db.Column(db.Integer ,primary_key=True)
    quote =db.Column(db.String(50) )
    openPrice =db.Column(db.String(50) )

@app.route('/',methods=['GET' ,'POST']) 
def main():

    if request.method =='POST':

        quote = request.form.get('quote')
        f=0
        if quote:
            r =requests.get(stock_url.format(quote)).json()
            if 'Message' in r.keys():
                 f=1
            else:
                stock_obj =Stock(quote=quote, openPrice=str(r['data'][0]['price_open']))
                db.session.add(stock_obj)
                db.session.commit()

        stock = Stock.query.all()

        stock_data=[]

        for i in stock:
            stocks={
                'id' :i.id,
                'quote' :i.quote,
                'open_price':i.openPrice
            }
            stock_data.append(stocks)
        
        return render_template('index2.html',stock_data=stock_data)

    else:
        return render_template('index.html')

if __name__=='main':
    app.run()




