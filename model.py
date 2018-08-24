#!/bin/usr/env python3

import sqlite3
import time
import datetime
from functools import lru_cache
import requests
import json
from random import randint


connection = sqlite3.connect("example.db")
cursor = connection.cursor()
@lru_cache()
def quote(ticker_symbol):
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
    response = requests.get(endpoint).text
    jsondata = json.loads(response)
    return jsondata.get('LastPrice', None)

def login(username, password):
    SQL = "SELECT pk FROM accounts WHERE username = ? AND password = ?"
    values = (username, password)
    cursor.execute(SQL, values)
    testvar = cursor.fetchone()
    if testvar == None:
        return None
    else:
        return testvar[0]

def save_create_account(username, password, balance):
  #  SQL = '''SELECT pk FROM accounts'''
  #  cursor.execute(SQL)
  #  all_pk = cursor.fetchall()
  #  max_pk = 0
  #  for i in all_pk:
  #      if int(*i) >= max_pk:
  #          max_pk == int(*i)
  #  pk = max_pk + 1
    #view.create_account()
   # create_username_password()
   # username = view.create_account[0]
   # password = view.create_account[1]
    funds = balance
    SQL2 = '''INSERT INTO accounts (username, password, balance) VALUES(?, ?, ?)'''
    values2 = (username, password, funds)
    cursor.execute(SQL2, values2)
    connection.commit()
 #   pk = True
#    return pk
#def create_username_password():
#    print('Please choose a username')
#    username = input()
#    print(username)
#    print()
#    print('OK, now choose a password')
#    password = input()
#    print(password)
#    print('Account succesfully created')
#    return(username, password)

def switch_accounts():
    pass




def get_accounts():
    SQL = '''SELECT pk, username, password, balance FROM accounts'''
    cursor.execute(SQL)
    accounts = cursor.fetchall()
    accounts_list = []
    for i in accounts:
        accounts_list.append(i)
    return accounts_list




def get_balance(pk):
   sql = "SELECT balance FROM accounts WHERE pk = ?"
   cursor.execute(sql, (pk,))
   balance = cursor.fetchone()
   connection.commit()
   if balance == None:
       return None
   else:
       return balance[0]

def get_holdings(pk):
    if pk == 1:
        input_vwap_TSLA(pk, 'TSLA')
        input_vwap_AAPL(pk, 'AAPL')
    SQL = "SELECT ticker_symbol, number_of_shares, volume_weighted_average_price FROM holdings WHERE account_pk = ?"
    values = (pk,)
    cursor.execute(SQL, values)
    testvar2 = cursor.fetchall()
    result = []
    for row in testvar2:
        dic = {
            "ticker_symbol":row[0],
            "number_of_shares":row[1],
            'volume_weighted_average_price': row[2]
        }
        result.append(dic)
    return result

def get_holding(pk, ticker_symbol):
   #connection = sqlite3.connect(‘example.db’, check_same_thread = False)
   #cursor = connection.cursor()
    sql = '''SELECT number_of_shares
 FROM holdings WHERE account_pk = ? and ticker_symbol = ?'''
    values = (pk, ticker_symbol.upper())
    cursor.execute(sql,values)
    holding = cursor.fetchall()
    holding_list = []
    connection.commit()
    for i in holding:
        if holding == None:
            return None
        else:
           return i[0]

def get_orders(pk, ticker_symbol, cutoff = '1970-01-01'):
    SQL = '''SELECT ticker_symbol,last_price, trade_volume, timestamp FROM
 orders WHERE account_pk = ? AND ticker_symbol = ? AND timestamp >= ?;'''
    cutoff_convert = int(time.mktime(datetime.datetime.strptime(cutoff, "%Y-%m-%d").timetuple()))
    values = (pk, ticker_symbol, cutoff_convert) #cutoff should be a string in yyyy-mm-dd format
    cursor.execute(SQL, values)
    lst = []
    rows = cursor.fetchall() #What data structure does rows return as? a list, or dict?
    for i in rows:
        d = {
        'ticker_symbol': i[0],
        'last_price': i[1],
        'trade_volume': i[2],
        'timestamp': '{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(i[3]))))}
        lst.append(d)
    return lst


def create_holding(account_pk, ticker_symbol, number_of_shares, price):
    SQL = '''INSERT INTO holdings (account_pk, ticker_symbol, number_of_shares, volume_weighted_average_price)
VALUES (?, ?, ?, ?)'''
    values = (account_pk, ticker_symbol.upper(), number_of_shares, create_vwap(account_pk, ticker_symbol, number_of_shares, price))
    cursor.execute(SQL, values)

def get_price(account_pk, ticker_symbol):
    SQL = '''SELECT last_price FROM orders WHERE account_pk = ? AND ticker_symbol =?'''
    values = (account_pk, ticker_symbol)
    cursor.execute(SQL, values)
    prices = cursor.fetchall()
    sum_prices = 0.00
    for i in prices:
        sum_prices += int(i[0])
    return sum_prices

def get_trade_volume(account_pk, ticker_symbol):
    SQL = '''SELECT trade_volume FROM orders WEHRE account_pk =? AND ticker_symbol = ?'''
    values = (account_pk, ticker_symbol)
    cursor.execute(SQL, values)


def select_all_tickers(account_pk):
    SQL = '''SELECT ticker_symbol FROM holdings WHERE account_pk = ?'''
    values = (account_pk,)
    cursor.execute(SQL, values)
    all_tickers = cursor.fetchall()
    ticker_list = []
    for i in all_tickers:
        ticker_list.append(i)
    return ticker_list

def input_vwap_TSLA(account_pk, ticker_symbol):
    SQL = '''SELECT last_price, trade_volume FROM orders WHERE account_pk = ?
AND ticker_symbol = ?'''
    values = (account_pk, ticker_symbol)
    cursor.execute(SQL, values)
    price_volume = cursor.fetchall()
    sum_buys_trade_volume = 0
    sum_trade_volume = 0
    for i in price_volume:
        if float(i[0]) > 0:
            sum_buys_trade_volume += (float(i[0]) *float(i[1]))
            sum_trade_volume += float(i[1])
    vwap = (sum_buys_trade_volume/sum_trade_volume)
    SQL_input = '''UPDATE holdings SET volume_weighted_average_price = ?
 WHERE account_pk = ? AND ticker_symbol = ?'''
    values_input = (vwap, account_pk, 'TSLA')
    cursor.execute(SQL_input, values_input)
    connection.commit()


def input_vwap_AAPL(account_pk, ticker_symbol):
    SQL = '''SELECT last_price, trade_volume FROM orders WHERE account_pk = ?
AND ticker_symbol = ?'''
    values = (account_pk, ticker_symbol)
    cursor.execute(SQL, values)
    price_volume = cursor.fetchall()
    sum_buys_trade_volume = 0
    sum_trade_volume = 0
    for i in price_volume:
        if float(i[0]) > 0:
            sum_buys_trade_volume += (float(i[0]) *float(i[1]))
            sum_trade_volume += float(i[1])
    vwap = (sum_buys_trade_volume/sum_trade_volume)
    SQL_input = '''UPDATE holdings SET volume_weighted_average_price = ?
 WHERE account_pk = ? AND ticker_symbol = ?'''
    values_input = (vwap, account_pk, 'AAPL')
    cursor.execute(SQL_input, values_input)
    connection.commit()


def create_vwap(account_pk, ticker_symbol, number_of_shares, price):
    volume_x_price = number_of_shares * price
    vwap = volume_x_price / number_of_shares
    return vwap


def modify_vwap(account_pk, ticker_symbol, number_of_shares, price):
    #endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
    #response = requests.get(endpoint).text
    #jsondata = json.loads(response)
    price = get_price(account_pk, ticker_symbol)
    #total_market_volume = jsondata.get('Volume', None)
    SQL = '''SELECT last_price, trade_volume From orders WHERE account_pk = ?
AND ticker_symbol = ?'''
    values = (account_pk, ticker_symbol)
    cursor.execute(SQL, values)
    price_volume = cursor.fetchall()
    sum_buys_trade_volume = 0
    sum_trade_volume = 0
    for i in price_volume:
        if float(i[0]) > 0:
            sum_buys_trade_volume += (float(i[0]) * float(i[1]))
            sum_trade_volume += float(i[1])
    #print(sum_buys_trade_volume)
    VWAP = (sum_buys_trade_volume/sum_trade_volume)
    return VWAP

def TWAP(ticker_symbol):
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
    response = requests.get(endpoint).text
    jsondata = json.loads(response)
    high = jsondata.get('High', None)
    low = jsondata.get('Low', None)
    close = jsondata.get('LastPrice', None)
    TWAP = (int(high) + int(low) +int(close))/3
    return TWAP

def modify_holding(account_pk, ticker_symbol, number_of_shares, price):
    SQL = '''UPDATE holdings SET number_of_shares = ?, volume_weighted_average_price =?
WHERE ticker_symbol = ? AND  account_pk = ?'''
    values = (number_of_shares, modify_vwap(account_pk, ticker_symbol, number_of_shares, price), ticker_symbol, account_pk)
    cursor.execute(SQL, values)
    connection.commit()

def modify_balance(account_pk, new_amount):
    SQL = '''UPDATE accounts SET balance = ? WHERE pk = ?'''
    cursor.execute(SQL,(new_amount, account_pk))
    connection.commit()

def create_order(account_pk, ticker_symbol, trade_volume, last_price):
    SQL = '''INSERT INTO orders (account_pk, ticker_symbol, last_price, trade_volume, timestamp)
            VALUES (?, ?, ?, ?, ?)'''
    values = (account_pk, ticker_symbol.upper(), last_price, trade_volume, int(time.time()))
    cursor.execute(SQL,values)
    connection.commit()


def buy(account_pk, ticker_symbol, volume):
   holding = get_holding(account_pk, ticker_symbol.upper())
   stock_price = quote(ticker_symbol.upper())
   if get_balance(account_pk) > (stock_price * volume):
       if holding != None:
           new_holding = holding + volume
           modify_holding(account_pk, ticker_symbol.upper(), new_holding, stock_price)
       else:
           create_holding(account_pk, ticker_symbol.upper(), volume, stock_price)

       new_balance = get_balance(account_pk) - (stock_price *volume)
       modify_balance(account_pk, new_balance)
       create_order(account_pk, ticker_symbol.upper(), volume, stock_price)
       return True
   else:
       return False

def sell(account_pk, ticker_symbol, number_of_shares):
    #Does my holding have enough shares
    number_of_current_shares = get_holding(account_pk, ticker_symbol.upper())
    if number_of_current_shares == None:
        return False
    elif number_of_current_shares < number_of_shares:
        return False
    else:
        #What is the share price?
        last_price = quote(ticker_symbol)
        #Calculate Remaining number of shares
        new_number_of_shares = get_holding(account_pk, ticker_symbol) - number_of_shares
        #Modify our Holdings
        modify_holding(account_pk, ticker_symbol, new_number_of_shares)
        #Modify Balance
        new_amount = get_balance(account_pk) + float(number_of_shares * last_price)
        modify_balance(account_pk, new_amount)
        #Create Order
        create_order(account_pk, ticker_symbol, number_of_shares, last_price)
        #Return True
        return True
