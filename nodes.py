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

def nodes():

    t = PrettyTable(['Name', 'URL', 'Port', 'SSL'])

    nodes = requests.get('https://raw.githubusercontent.com/turtlecoin/turtlecoin-nodes-json/master/turtlecoin-nodes.json').json()
    nodes = nodes['nodes']

    for node in nodes:
      
      node_name = Fore.GREEN + node['name'] + Fore.RESET
      url_link = Fore.GREEN + node['url'] + Fore.RESET
      port_no = Fore.YELLOW + str(node['port']) + Fore.RESET
      
      if node['ssl']:
            ssl_status = Fore.GREEN + str(node['ssl']) + Fore.RESET
      else:
            ssl_status = Fore.RED + str(node['ssl']) + Fore.RESET
     
      t.add_row([node_name, url_link, port_no, ssl_status])
    
    table = t.copy()
    t.clear_rows()
   
    return {'table': table}
