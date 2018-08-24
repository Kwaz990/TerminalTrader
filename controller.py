import model
import view

if __name__ == "__main__":
    exit_terminal = False
    while exit_terminal == False:
        global pk
        pk = None
        view.welcome()
        selection = view.initial_prompt()
        if selection.strip() == '1' or selection.strip() == 'LOG IN' or selection.strip() == 'log in':
            username, password = view.login_prompt()
            pk = model.login(username, password)
            exit_terminal = True
            view.pause()
        elif selection.strip() == '2' or selection.strip() == 'CREATE ACCOUNT' or selection.strip() == 'create account':
            username, password, balance = view.create_account()
            pk = model.save_create_account(username, password, balance)
            exit_terminal == True
    while pk == None:
        username, password = view.login_prompt(True)
        pk = model.login(username, password)
    exit_terminal = False
    while exit_terminal == False:
        option = view.main_menu()
        if option.strip() == "0":
            exit_terminal = True
        elif option.strip() == "1":
            balance = model.get_balance(pk)
            holdings = model.get_holdings(pk)
            view.show_status(balance, holdings)
            view.pause()
        elif option.strip() == '3':
            ticker_symbol, number_of_shares = view.sell_menu()
            status = model.sell(pk, ticker_symbol, number_of_shares)
            if status == False:
                view.sell_error()
                view.pause()
            else:
                view.sell_good()
                view.pause()
        elif option.strip() == '5':
           ticker_symbol = view.quote_prompt()
           quote = model.quote(ticker_symbol)
           view.display_quote(ticker_symbol, quote)
           view.pause()
        elif option.strip() == "2":
           account_pk = pk
           ticker_symbol = view.getsymbol()
           number_of_shares = view.volume()
           finalbuy = model.buy(account_pk, ticker_symbol,number_of_shares)
           if finalbuy == False:
               view.failuremessage()
           else:
               view.successmessage()
        elif option.strip() == "4":
           account_pk = pk
           ticker_symbol = view.ticker_request()
           orders = model.get_orders(account_pk, ticker_symbol)
           view.display_order_hist(account_pk, ticker_symbol,orders)
        elif option.strip() == '6':
            username, password, balance = view.create_account()
            model.save_create_account(username, password, balance)
        elif option.strip() == '7':
            switch = view.switch_accounts()
            if switch == True:
                view.pause()
                pk = None
                view.switch_success()
                view.welcome()
                username, password = view.login_prompt()
                pk = model.login(username, password)
            elif switch == False:
                view.switch_fail()
