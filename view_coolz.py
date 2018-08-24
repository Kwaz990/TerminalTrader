#!/bin/usr/env python3

def login_prompt(error = False):
    if error:
        print('login Incorect!')
    username = input('Username: ')
    password = input('Password: ')
    return username, password

def welcome():
#    print('Welcome to Terminal Trader')

#     n must be odd and m = n*3
    n = 11
    m = 33

    unit = '.|.'

    for i in reversed(range((n))[::2]):
        if i == 0:
            pass
        else:
            print('{}'.center(m - (len(unit*(n-i)))+2, '-').format(unit*(n-i)))

    print('WELCOME TO TERIMNAL TRADER'.center(m, '-'))

    for i in range(n)[::2]:
        if i == 0:
            pass
        else:
            print('{}'.center(m - (len(unit*(n-i)))+2, '-').format(unit*(n-i)))

def main_menu():
    welcome()
    print()
    print()
    print('Main Menu')
    print('Options: ')
    print('0) Exit')
    print('1) Account Balance & Holdings')
    print()
    selection = input('Which Option?: ')
    return selection

def pause():
    input('Okay?')
    print('\n\n\n\n\n')

def show_status(balance, holdings):
    print('Balance: ', balance)
#    pretty_holdings = [*i for i in holdings]

    def pretty_holdings():
        print('{:<8} {:<10}'.format('Ticker Symbol', 'Number of Shares'))
        for key in holdings:
            print('{!s:<8s}'.format(key))
#    for i in holdings:
#        print(*i)
#            return('{!s:<20s}'.format(i))
    print('Holdings: ', pretty_holdings())

