from prettytable import PrettyTable
import requests

from colorama import Fore, Style, init
init()

print(Fore.YELLOW + 'Retrieving pool status.. \nYou may have to maximise the window in order to see the data correctly\n' + Fore.RESET)

t = PrettyTable(['Pool Height', 'Hashrate', 'Miners', 'Total Fee', 'Min. Payout', 'Time of Last Block Found', 'Height of Last Block Found'])

pools = requests.get('https://raw.githubusercontent.com/turtlecoin/turtlecoin-pools-json/master/v2/turtlecoin-pools.json').json()

err_msg = Fore.RED + 'Could not retrieve information, please try again'

#print(pools)

for pool in pools['pools']:
    try:
        pool_api = pool['api']
    except KeyError: # no api
        pool_api = '-'

    print(pool_api)