#!/bin/usr/env python3


import time


def initial_prompt():
    print('1) LOG IN')
    print('2) CREATE ACCOUNT')
    selection = input('Please select an option: ')
    return selection


def login_prompt(error = False):
    if error:
        print("LOGIN INCORRECT!!")
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    return username, password

def welcome():
# n must be off and m = n*3
    n = 11
    m = 33
    unit = '.|.'
    for i in reversed(range((n))[::2]):
        if i == 0:
            pass
        else:
            print('{}'.center(m - (len(unit*(n-i)))+2, '-').format(unit*(n-i)))
    print("WELCOME TO TERMINAL TRADER!".center(m, '-'))
    for i in range(n)[::2]:
        if i == 0:
            pass
        else:
            print('{}'.center(m - (len(unit*(n-i)))+2, '-').format(unit*(n-i)))


def main_menu():
    print("MAIN MENU")
    print("OPTIONS:")
    print("0) EXIT")
    print("1) ACCOUNT BALANCE AND HOLDINGS")
    print('2) BUY')
    print('3) SELL')
    print('4) ORDER HISTORY')
    print('5) QUOTE')
    print('6) CREATE ACCOUNT')
    print('7) SWITCH ACCOUNTS')
    print()
    selection = input("WHICH OPTION DO YOU CHOOSE? ")
    return selection

def pause():
    input("processing...")
    print("\n\n\n")


def sell_menu():
    print('What would you like to sell?')
    ticker_symbol = input()
    print(ticker_symbol)
    print('How much of {} would you like to sell?'.format(ticker_symbol))
    number_of_shares = int(input())
    print(number_of_shares)
    return (ticker_symbol, number_of_shares)


def sell_error():
    print('Sorry, you don\'t have enough shares.')
    print('Would you like to choose another option?')
    print()
    print()

def sell_good():
    print('Sale complete!.')


def quote_prompt():
   ticker_symbol = str(input('Which ticker symbol do you want to see the price?')).upper()
   return ticker_symbol

def display_quote(ticker_symbol,quote):
   print('The quote for {} is {}.'.format(ticker_symbol,quote))


def failuremessage():
   print("Insufficient funds!\n\n\n")
   pause()

def successmessage():
   print("Good job !\n\n\n")
   pause()

def getsymbol():
   symb = str(input("Please input your ticker symbol: ")).upper()
   return symb

def volume():
   volume = float(input("Please input the number of shares: "))
   return volume

def show_status(balance, holdings):
   print("{0:^40}".format("BALANCE:"))
   print("{0:^40}".format(balance),"\n")
   print("{0:^40}".format("HOLDINGS:"))
   print("{0:^20}{1:^20}{2:^20}".format("TICKER SYMBOL","NUMBER OF SHARES", 'VOLUME WEIGHTED AVERAGE PRICE'))
   for holding in holdings:
       print("{:^20}{:^20}{:^20}\n".format(holding["ticker_symbol"], holding['number_of_shares'], holding['volume_weighted_average_price']), end='')
      # print("{0:^20}".format(holding["number_of_shares"]), end='\n')
      # print('{!s:^30}'.format(holding['volume_weighted_average_price']))

def ticker_request():
   ticker = str(input("PLEASE ENTER THE TICKER SYMBOL YOU WANT TO SEE ORDER HISTORY FOR: ")).upper()
   return ticker

def display_order_hist(account_pk, ticker_symbol, orders):
   print()
   print()
   print("{0:^60}".format("ORDER HISTORY FOR "))
   print()
   print('{0:^60}'.format(ticker_symbol.upper()))
   print("\n\n")
   print("{0:^20}{1:^20}{2:^20}\n".format("TIME STAMP", "TRADE VOLUME", "LAST PRICE"))
   for stocks in orders:
      # print("{!s:^16}".format(time.localtime(int(stocks["timestamp"]))),end='')
       print("{0:^20}".format(stocks['timestamp']), end='')
#       print("{0:^20}".format(time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(stocks['timestamp'])))), end='')
       print("{0:^20}".format(stocks["trade_volume"]),end='')
       print("{0:^20}".format(stocks["last_price"]),end='\n')
   print("\n\n")

def create_account():
    username = input('Please choose a username: ')
    password = input('Please choose a password: ')
    balance = input('Please make a deposit to fund your account: ')
    pause()
    print('Account succsfully created')
    return username, password, balance


def switch_accounts():
    print('Are you sure you want to log off and switch accounts?')
    ans = input('Y or N:' )
    print(ans)
    if ans == 'y' or ans == 'yes' or ans == 'Y' or ans == 'Yes' or ans =='YES' :
        return True
    elif ans == 'n' or ans == 'no' or ans == 'N' or ans == 'No' or ans == 'NO':
        return False


def switch_success():
    print('Okay, logging off.')

def switch_fail():
    print('Okay.')
