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
    balance =db.Column(db.String(50) ,nullable=False)
    quote =db.Column(db.String(50) )
    shares =db.Column(db.String(50) )

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
                stock_obj =Stock(balance ='10000' ,quote=quote ,shares='0')
                db.session.add(stock_obj)
                db.session.commit()
        quote ='AAPL,MSFT,HSBA.L'
        return render_template('index2.html',quote_name=quote)

    else:
        stock = Stock.query.all()
        stock_data=[]
        for i in stock:
            stock_data.append(i.quote)
    
        return render_template('index.html',stock_data=stock_data)


if __name__=='main':
    app.run()




