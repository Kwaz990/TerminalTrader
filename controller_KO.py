#!/bin/usr/env python3 


import model
import view


if __name__== '__main__':
    pk = None
    view.welcome()
    username, password = view.login_prompt()
    pk = model.login(username, password)
    while pk == None:
        username, password = view.login_prompt(True)
        pk = model.login(username, password)
    exit_terminal = False
    while exit_terminal == False:
        option = view.main_menu()
        if option.strip() == 0:
            exit_terminal == True
        elif option.strip() == '1':
            balance = model.get_balance(pk)
            holdings = model.get_holdings(pk)
            view.show_status(balance, holdings)
            view.pause()


