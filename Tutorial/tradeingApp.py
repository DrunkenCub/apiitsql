import os

from flask import Flask
from flask import render_template
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.sql import text
import datetime

engine = create_engine('mysql+pymysql://root:root@localhost:3306/tradeapp')
Base = declarative_base()
Base.metadata.reflect(engine)

SECRET_KEY = 'develop'
app = Flask(__name__)
app.config.from_object(__name__)

from sqlalchemy.orm import relationship, backref

class Users(Base):
    __table__ = Base.metadata.tables['users']

class BitCoinValues(Base):
    __table__ = Base.metadata.tables['bitcoinvalues']

class Trades(Base):
    __table__ = Base.metadata.tables['trades']

class Messages(Base):
    __table__ = Base.metadata.tables['messages']

from functools import wraps
from flask import g, request, redirect, url_for, session


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            print (session['uid'])
        except:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/add-users", methods=["GET", "POST"])
@login_required
def add_users():
    db_session = scoped_session(sessionmaker(bind=engine))
    if request.form:
        request_data = request.form
        statement = text("""INSERT INTO Users (username, password, email, address, mobile, deposit) 
                            values (:username, :password, :email, :address, :mobile, :deposit)""")
        engine.execute(statement, 
                        username=request_data['username'],
                        password=request_data['password'], 
                        email=request_data['email'], 
                        address=request_data['address'], 
                        mobile=request_data['mobile'], 
                        deposit=request_data['deposit'])
    return render_template("addusers.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.form:
        request_data = request.form
        statement = text("""SELECT * from Users WHERE username=:username AND password = :password""")
        result = engine.execute(statement, 
                                username=request_data['username'], 
                                password=request_data['password']).fetchone()
        if len(result) == 0:
            return redirect(url_for('login', next=request.url))
        else:
            session['uid'] = result['uid']
            return redirect(url_for('add_users', next=request.url))
    return render_template("login.html")

@app.route('/trade', methods=["GET", "POST"])
@login_required
def trade():
    if request.form:
        request_data = request.form
        statement =  text("""INSERT INTO trades (tradedate, userid, bitcoinid, amount) 
                            values (:tradedate, :userid, :bitcoinid, :amount)""")
        amount = float(request_data['buyamount']) - float(request_data['sellamount'])
        print (amount)
        result = engine.execute(statement, 
                                tradedate=datetime.datetime(2012, 2, 23, 0, 0).strftime('%m/%d/%Y'),
                                userid=session['uid'],
                                bitcoinid=1,
                                amount=amount
                                )
    return render_template('trade.html', value=None)   





@app.route('/')
@login_required
def home():
    pass


if __name__ == "__main__":
    app.run(debug=True)