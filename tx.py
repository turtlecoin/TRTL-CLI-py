from turtlecoin import TurtleCoind
from prettytable import PrettyTable
import locale
from colorama import Fore, Style, init
init(autoreset=True)

tc = TurtleCoind('public.turtlenode.io')

t = PrettyTable(['Amount', 'Fee', 'Size', 'Hash', 'Confirmed'])

f = open('ascii/walker.txt')
walker_ascii = f.read()
f.close

locale.setlocale(locale.LC_ALL, '')

def txs(hash=False):

    txs = tc.get_transaction_pool() # get mempool
    mempool = txs['result']['transactions'] # make var

    if hash and len(hash) != 64:
        print(Fore.RED + "Invalid hash!")
        return {'tx_info': ''}

    if hash:
        try:
            ###################
            # TX IS CONFIRMED #
            ###################
            tx_is_confirmed = tc.get_transaction(hash)
            if tx_is_confirmed:
                ctx_info = tx_is_confirmed['result']['txDetails']

                ctx_amount_shells = ctx_info['amount_out'] / 100
                ctx_amount = Fore.GREEN + locale.currency(ctx_amount_shells, symbol=False, grouping=True) + Fore.RESET
                ctx_fee = Fore.GREEN + str(ctx_info['fee'] / 100) + Fore.RESET
                ctx_size = Fore.GREEN + str(ctx_info['size']) + Fore.RESET
                ctx_hash = Fore.YELLOW + ctx_info['hash'] + Fore.RESET

                t.add_row([ctx_amount, ctx_fee, ctx_size, ctx_hash, Fore.GREEN + "Yes" + Fore.RESET])

                table = t.copy()
                t.clear_rows()
                
                return {'tx_info': table}

        except ValueError: # not confirmed
            try:
                ####################################
                # TX IS IN MEMPOOL AND UNCONFIRMED #
                ####################################
                for transac in mempool:
                    if transac['hash'] == hash:
                        uctx_amount_shells = transac['amount_out'] / 100
                        uctx_amount = Fore.GREEN + locale.currency(uctx_amount_shells, symbol=False, grouping=True) + Fore.RESET
                        uctx_fee = Fore.GREEN + str(transac['fee'] / 100) + Fore.RESET
                        uctx_size = Fore.GREEN + str(transac['size']) + Fore.RESET
                        uctx_hash = Fore.YELLOW + transac['hash'] + Fore.RESET
                        
                        t.add_row([uctx_amount, uctx_fee, uctx_size, uctx_hash, Fore.RED + "No" + Fore.RESET])

                        table = t.copy()
                        t.clear_rows()
                        
                        return {'tx_info': table}
                    else:
                        raise Exception
                        # go into except statement reee

            except:
                ######################
                # TX IS NON EXISTENT #
                ######################
                print("\nCould not find supplied tx! Meanwhile, here's a turtle!")
                return {'tx_info': walker_ascii}
                # returning ascii since too lazy

    else:
        if len(mempool) > 0:

            for txa in mempool:
                #################
                # SHOWS MEMPOOL #
                #################
                amount_shells = txa['amount_out'] / 100
                amount = Fore.GREEN + locale.currency(amount_shells, symbol=False, grouping=True) + Fore.RESET
                fee = Fore.GREEN + str(txa['fee'] / 100) + Fore.RESET
                size = Fore.GREEN + str(txa['size']) + Fore.RESET
                hash = Fore.YELLOW + txa['hash'] + Fore.RESET

                t.add_row([amount, fee, size, hash, Fore.RED + "No" + Fore.RESET])
        
            table = t.copy()
            t.clear_rows()

            return {'tx_info': table}

        else:
            ####################
            # MEMPOOL IS EMPTY #
            ####################
            print("\nNo transactions to show! Here's a turtle instead!")
            return {'tx_info': walker_ascii}
            # returning ascii since too lazy


# ill come back another day to fix this up




#soon(tm)