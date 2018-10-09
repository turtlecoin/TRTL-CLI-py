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

import requests
from prettytable import PrettyTable

from colorama import Fore, Style, init
init(autoreset=True) #init the colored stuff so it works on windows. autoreset resets it back to set cmd color by default every time

def pool():

    print(Fore.YELLOW + 'Retrieving pool status.. \nYou may have to maximise the window in order to see the data correctly\n' + Fore.RESET)

    t = PrettyTable(['Name', 'URL', 'API', 'Type', 'Mining Address'])

    pools = requests.get('https://raw.githubusercontent.com/turtlecoin/turtlecoin-pools-json/master/v2/turtlecoin-pools.json').json()

    for x in pools['pools']:

        pool_name = Fore.GREEN + x['name'] + Fore.RESET
        pool_url = Fore.GREEN + x['url'] + Fore.RESET

        try:
            pool_api = Fore.YELLOW + x['api'] + Fore.RESET
        except KeyError: # no api
            pool_api = Fore.YELLOW + '-' + Fore.RESET

        pool_type = Fore.YELLOW + x['type'] + Fore.RESET

        pool_address = Fore.GREEN + x['miningAddress'] + Fore.RESET

        t.add_row([pool_name, pool_url, pool_api, pool_type, pool_address])
    
    table = t.copy()
    t.clear_rows()
    return {'table': table}