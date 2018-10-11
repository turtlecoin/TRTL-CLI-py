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
import locale
from datetime import datetime

from colorama import Fore, Style, init
init(autoreset=True) #init the colored stuff so it works on windows. autoreset resets it back to set cmd color by default every time

data = ''
pool_type = ''
api_link = ''
locale.setlocale(locale.LC_ALL, '') # set locale for the commas 

def pool():

    print(Fore.YELLOW + 'Retrieving pools\' status.. \nYou may have to maximise the window in order to see the data correctly\n' + Fore.RESET)

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


def onepool(input):
    global data
    global pool_type
    global api_link

    print(Fore.YELLOW + 'Retrieving pool status.. \nYou may have to maximise the window in order to see the data correctly\n' + Fore.RESET)

    t = PrettyTable(['Pool Height', 'Hashrate', 'Miners', 'Total Fee', 'Min. Payout', 'Time of Last Block Found', 'Height of Last Block Found'])

    pools = requests.get('https://raw.githubusercontent.com/turtlecoin/turtlecoin-pools-json/master/v2/turtlecoin-pools.json').json()

    err_msg = Fore.RED + 'Could not retrieve information, please try again'

    for pool in pools['pools']:
        try:
            if input == pool['name'].lower() or input == pool['url'].lower() or input == pool['api'].lower() or input == pool['miningAddress'].lower(): # array has problems
                
                pool_type = pool['type']

                api_link = pool['api']

                if pool_type == 'forknote' or pool_type == 'forknote-alt':
                    
                    api_link += 'stats'
                    height_api_link = False
                    config_api_link = False
                
                else:

                    height_api_link = api_link + 'network/stats'
                    config_api_link = api_link + 'config'
                    api_link += 'pool/stats'

                try:
                    data = requests.get(api_link).json()

                    if height_api_link and config_api_link:
                        network_data = requests.get(height_api_link).json()
                        config_data = requests.get(config_api_link).json()
                    
                except:
                    data = False
                    network_data = False
                    config_data = False
                
            else:
                pass

        except: # that one entry which doesnt have an api link
            pass

    if pool_type == 'forknote':

        if data: # only need data here

            pool_height = data['network']['height']
            pool_height = Fore.GREEN + str(pool_height) + Fore.RESET
            
            pool_hr_hashes = data['pool']['hashrate']
            number_of_hr_units = len(str(pool_hr_hashes))
        
            if number_of_hr_units > 3:
                pool_hr_khashes = pool_hr_hashes / 1000
            else:
                pool_hr_khashes = False
            
            if pool_hr_khashes:
                number_of_khs_units = len(str(int(pool_hr_khashes)))
        
                if number_of_khs_units > 3:
                    pool_hr_mhashes = pool_hr_khashes / 1000
                else:
                    pool_hr_mhashes = False
            else:
                pool_hr_mhashes = False

            if pool_hr_mhashes:
                hashes = str(round(pool_hr_mhashes, 2)) + " MH/s"
            elif pool_hr_khashes:
                hashes = str(round(pool_hr_khashes, 2)) + ' KH/s'
            else:
                hashes = str(round(pool_hr_hashes, 2)) + ' H/s'

            hashes = Fore.GREEN + hashes + Fore.RESET
            
            pool_miners = data['pool']['miners']
            pool_miners_commas = locale.currency(pool_miners, symbol=False, grouping=True)
            miners = str(int(float(pool_miners_commas))) + ' miners'
            miners = Fore.GREEN + str(miners) + Fore.RESET

            pool_fee = data['config']['fee']
            fee = str(pool_fee) + ' TRTL'
            fee = Fore.YELLOW + fee + Fore.RESET

            pool_min_payout_shells = data['config']['minPaymentThreshold'] / 100
            pool_min_payout = locale.currency(pool_min_payout_shells, symbol=False, grouping=True)
            min_pay = str(pool_min_payout) + ' TRTL'
            min_pay = Fore.YELLOW + min_pay + Fore.RESET

            pool_block_found_epoch = data['pool']['lastBlockFound']
            pool_block_found_10chars_epoch = str(pool_block_found_epoch)[:10]
            pool_block_found = datetime.fromtimestamp(int(pool_block_found_10chars_epoch))
            block_found = str(pool_block_found)
            block_found = Fore.GREEN + block_found + Fore.RESET

            pool_block_height = data['pool']['blocks'][1]
            block_height = Fore.GREEN + pool_block_height + Fore.RESET

            t.add_row([pool_height, hashes, miners, fee, min_pay, block_found, block_height])

            table = t.copy()
            t.clear_rows()
            return {'pool': table}
        else:
            return {'pool': err_msg}

    elif pool_type == 'node.js':

        if data and config_data and network_data: # need all here
        
            pool_height = str(network_data['height'])
            pool_height = Fore.GREEN + pool_height + Fore.RESET

            pool_hr_hashes = data['pool_statistics']['hashRate']
            number_of_hr_units = len(str(pool_hr_hashes))
        
            if number_of_hr_units > 3:
                pool_hr_khashes = pool_hr_hashes / 1000
            else:
                pool_hr_khashes = False
            
            if pool_hr_khashes:
                number_of_khs_units = len(str(int(pool_hr_khashes)))
        
                if number_of_khs_units > 3:
                    pool_hr_mhashes = pool_hr_khashes / 1000
                else:
                    pool_hr_mhashes = False
            else:
                pool_hr_mhashes = False

            if pool_hr_mhashes:
                hashes = str(round(pool_hr_mhashes, 2)) + ' MH/s'
            elif pool_hr_khashes:
                hashes = str(round(pool_hr_khashes, 2)) + ' KH/s'
            else:
                hashes = str(round(pool_hr_hashes, 2)) + 'H/s' 

            hashes = Fore.GREEN + hashes + Fore.RESET
        
            pool_miners = data['pool_statistics']['miners']
            pool_miners_commas = locale.currency(pool_miners, symbol=False, grouping=True)
            miners = str(int(float(pool_miners_commas))) + ' miners'
            miners = Fore.GREEN + str(miners) + Fore.RESET
            
            pool_fee = config_data['pplns_fee']
            fee = str(pool_fee) + ' TRTL'
            fee = Fore.YELLOW + fee + Fore.RESET

            pool_min_payout_shells = config_data['min_wallet_payout'] / 100
            pool_min_payout = locale.currency(pool_min_payout_shells, symbol=False, grouping=True)
            min_pay = str(pool_min_payout) + ' TRTL'
            min_pay = Fore.YELLOW + min_pay + Fore.RESET

            pool_block_found_epoch = data['pool_statistics']['lastBlockFoundTime']
            pool_block_found_10chars_epoch = str(pool_block_found_epoch)[:10]
            pool_block_found = datetime.fromtimestamp(int(pool_block_found_10chars_epoch))
            block_found = str(pool_block_found)
            block_found = Fore.GREEN + block_found + Fore.RESET

            pool_block_height = data['pool_statistics']['lastBlockFound']
            block_height = Fore.GREEN + str(pool_block_height) + Fore.RESET

            t.add_row([pool_height, hashes, miners, fee, min_pay, block_found, block_height])

            table = t.copy()
            t.clear_rows()
            return{'pool': table}

        else:
            return {'pool': err_msg}

    else: # forknote-alt

        if data: # only data needed here

            pool_height = str(data['network']['height'])
            pool_height = Fore.GREEN + pool_height + Fore.RESET
            
            pool_hr_hashes = data['pool']['hashrate']
            number_of_hr_units = len(str(pool_hr_hashes))
        
            if number_of_hr_units > 3:
                pool_hr_khashes = pool_hr_hashes / 1000
            else:
                pool_hr_khashes = False
            
            if pool_hr_khashes:
                number_of_khs_units = len(str(int(pool_hr_khashes)))
        
                if number_of_khs_units > 3:
                    pool_hr_mhashes = pool_hr_khashes / 1000
                else:
                    pool_hr_mhashes = False
            else:
                pool_hr_mhashes = False

            if pool_hr_mhashes:
                hashes = str(round(pool_hr_mhashes, 2)) + " MH/s"
            elif pool_hr_khashes:
                hashes = str(round(pool_hr_khashes, 2)) + ' KH/s'
            else:
                hashes = str(round(pool_hr_hashes, 2)) + ' H/s'

            hashes = Fore.GREEN + hashes + Fore.RESET

            pool_miners = data['pool']['miners']
            pool_miners_commas = locale.currency(pool_miners, symbol=False, grouping=True)
            miners = str(int(float(pool_miners_commas))) + ' miners'
            miners = Fore.GREEN + str(miners) + Fore.RESET

            pool_fee = data['config']['fee']
            fee = str(pool_fee) + ' TRTL'
            fee = Fore.YELLOW + fee + Fore.RESET

            pool_min_payout_shells = data['config']['minPaymentThreshold'] / 100
            pool_min_payout = locale.currency(pool_min_payout_shells, symbol=False, grouping=True)
            min_pay = str(pool_min_payout) + ' TRTL'
            min_pay = Fore.YELLOW + min_pay + Fore.RESET

            pool_block_found_epoch = data['lastblock']['timestamp']
            pool_block_found_10chars_epoch = str(pool_block_found_epoch)[:10]
            pool_block_found = datetime.fromtimestamp(int(pool_block_found_10chars_epoch))
            block_found = str(pool_block_found)
            block_found = Fore.GREEN + block_found + Fore.RESET

            pool_block_height = data['lastblock']['height']
            block_height = Fore.GREEN + str(pool_block_height) + Fore.RESET

            t.add_row([pool_height, hashes, miners, fee, min_pay, block_found, block_height])

            table = t.copy()
            t.clear_rows()
            return {'pool': table}

        else:
            return {'pool': err_msg}