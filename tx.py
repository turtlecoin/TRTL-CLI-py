"""
	Copyright (C) 2018 Sajo8

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from turtlecoin import TurtleCoind
from prettytable import PrettyTable
import locale
from colorama import Fore, Style, init
init(autoreset=True)

tc = TurtleCoind('public.turtlenode.io') # init turtlecoind

t = PrettyTable(['Amount', 'Fee', 'Size', 'Hash', 'Confirmed']) # init table

f = open('ascii/walker.txt')
walker_ascii = f.read() # make ascii art to printif needed
f.close

locale.setlocale(locale.LC_ALL, '') # set locale for the commas 

def txs(hash=False):

    txs = tc.get_transaction_pool() # get mempool
    mempool = txs['result']['transactions'] # make var

    if hash and len(hash) != 64: # if arg given is less or more than 64
        print(Fore.RED + "Invalid hash!") # invalid
        return {'tx_info': ''}
        # returning empty dict since too lazy

# hash can be invalid even if 64 characters but whatevs

    if hash:
        try:
            ###################
            # TX IS CONFIRMED #
            ###################
            tx_is_confirmed = tc.get_transaction(hash) # store it in a var
            if tx_is_confirmed: # if the tx is confirmed
                ctx_info = tx_is_confirmed['result']['txDetails'] # make details easy to retrieve

                ctx_amount_shells = ctx_info['amount_out'] / 100 # get shells and convert to turtles
                ctx_amount = Fore.GREEN + locale.currency(ctx_amount_shells, symbol=False, grouping=True) + Fore.RESET # add color and commas to turtles
                ctx_fee = Fore.GREEN + str(ctx_info['fee'] / 100) + Fore.RESET # fee, from shells to turtles
                ctx_size = Fore.GREEN + str(ctx_info['size']) + Fore.RESET # size of the thing
                ctx_hash = Fore.YELLOW + ctx_info['hash'] + Fore.RESET # hash

                t.add_row([ctx_amount, ctx_fee, ctx_size, ctx_hash, Fore.GREEN + "Yes" + Fore.RESET]) # add it to table

                table = t.copy() # copy table to another var
                t.clear_rows() #clear table's rows
                
                return {'tx_info': table} # return the table

        except ValueError: # not confirmed
            try:
                ####################################
                # TX IS IN MEMPOOL AND UNCONFIRMED #
                ####################################
                for transac in mempool: # goes through every tx in the mempool
                    if transac['hash'] == hash: # if the hash is equal to given hash

                        # basically do the same thing again, see the try statement

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
                        # not in the mempool
                        raise Exception
                        # force it to go into the except statement

            except:
                ######################
                # TX IS NON EXISTENT #
                ######################
                print("\nCould not find supplied tx! Meanwhile, here's a turtle!")
                return {'tx_info': walker_ascii}
                # returning ascii since too lazy

    else: # no hash given
        if len(mempool) > 0:
            # txs in in mempool exist

            for txa in mempool:
                #################
                # SHOWS MEMPOOL #
                #################

                # again the same thing, see the first try statement
                
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