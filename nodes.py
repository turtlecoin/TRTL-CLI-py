import requests
from prettytable import PrettyTable

from colorama import Fore, Style, init
init(autoreset=True) #init the colored stuff so it works on windows. autoreset resets it back to set cmd color by default every time

def nodes():

    t = PrettyTable(['Name', 'URL', 'Port', 'SSL'])

    nodes = requests.get('https://raw.githubusercontent.com/turtlecoin/turtlecoin-nodes-json/master/turtlecoin-nodes.json').json()

    for x in nodes['nodes']:
        node_name = Fore.GREEN + x['name'] + Fore.RESET
        url_link = Fore.GREEN + x['url'] + Fore.RESET
        port_no = Fore.YELLOW + str(x['port']) + Fore.RESET
        if x['ssl']:
            ssl_status = Fore.GREEN + str(x['ssl']) + Fore.RESET
        else:
            ssl_status = Fore.RED + str(x['ssl']) + Fore.RESET

        t.add_row([node_name, url_link, port_no, ssl_status])
    return {'table': t}
