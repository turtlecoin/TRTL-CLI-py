import grequests
import requests
import locale
from prettytable import PrettyTable
from datetime import datetime

from colorama import Fore, Style, init
init()

table = None

def allpools():
	global table

	locale.setlocale(locale.LC_ALL, '') # set locale for the commas 

	print(Fore.YELLOW + 'Retrieving pool status.. \nYou may have to maximise the window in order to see the data correctly\n' + Fore.RESET)
	print(Fore.YELLOW + 'This may take a while, hang on!\n' + Fore.RESET)

	t = PrettyTable(['Pool Name', 'Pool URL', 'Pool Height', 'Hashrate', 'Miners', 'Total Fee', 'Min. Payout', 'Time of Last Block Found', 'Height of Last Block Found'])

	pools = requests.get("https://raw.githubusercontent.com/turtlecoin/turtlecoin-pools-json/master/v2/turtlecoin-pools.json").json()

	err_msg = Fore.RED + 'Could not retrieve information, please try again'
	no_stats = Fore.RED + 'Couldn\'t retrieve stats' + Fore.RESET
	red_hyphen = Fore.RED + '---' + Fore.RESET

	for pool in pools['pools']:

		pool_name = Fore.GREEN + pool['name'] + Fore.RESET

		pool_type = pool['type']

		api_link = pool['api']

		pool_url = Fore.GREEN + pool['url'] + Fore.RESET

		if pool_type == 'forknote' or pool_type == 'forknote-alt':
					
			api_link += 'stats'
			height_api_link = False
			config_api_link = False
				
		elif pool_type == 'node.js':

			height_api_link = api_link + 'network/stats'
			config_api_link = api_link + 'config'
			api_link += 'pool/stats'
		
		else: # cryptonote social
			height_api_link = False
			config_api_link = False
			# dont mess with api link
		
		try:

			if height_api_link and config_api_link: # node js
				
				urls = [api_link, height_api_link, config_api_link]

				rs = (grequests.get(url, timeout=3) for url in urls)
				all_results = grequests.map(rs)

				data_assigned = 0 # so that we can assign appropriate response values to proper variable

				for single_request in all_results:

					
					if data_assigned == 0:
						data = single_request.json()
						data_assigned += 1
						continue
					elif data_assigned == 1:
						network_data = single_request.json()
						data_assigned += 1
						continue
					else:
						config_data = single_request.json()

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
						if int(float(pool_miners_commas)) != 1:
								miner_amount = ' miners'
						else:
							miner_amount = ' miner'
						miners = str(int(float(pool_miners_commas))) + miner_amount
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

						t.add_row([pool_name, pool_url, pool_height, hashes, miners, fee, min_pay, block_found, block_height])

						table = t.copy()
					
					else:
						t.add_row([err_msg, err_msg, err_msg, err_msg, err_msg, err_msg, err_msg, err_msg])
						table = t.copy()

					continue

			else:
				
				urls = [api_link]

				dt = (grequests.get(url, timeout=3) for url in urls)
				all_data = grequests.map(dt)
				
				for single_response in all_data:
					data = single_response.json()

					if pool_type == 'forknote':

						if data:

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
							if int(float(pool_miners_commas)) != 1:
								miner_amount = ' miners'
							else:
								miner_amount = ' miner'
							miners = str(int(float(pool_miners_commas))) + miner_amount
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

							t.add_row([pool_name, pool_url, pool_height, hashes, miners, fee, min_pay, block_found, block_height])

							table = t.copy()

						else:
							t.add_row([err_msg, err_msg, err_msg, err_msg, err_msg, err_msg, err_msg, err_msg, err_msg])
							table = t.copy()

						continue
					
					elif pool_type == 'forknote-alt':

						if data:

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
							if int(float(pool_miners_commas)) != 1:
								miner_amount = ' miners'
							else:
								miner_amount = ' miner'
							miners = str(int(float(pool_miners_commas))) + miner_amount
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

							t.add_row([pool_name, pool_url, pool_height, hashes, miners, fee, min_pay, block_found, block_height])

							table = t.copy()

						else:
							pass

						continue
							
		except Exception as e:
			t.add_row([pool_name, pool_url, no_stats, red_hyphen, red_hyphen, red_hyphen, red_hyphen, red_hyphen, red_hyphen])
			data = False
			network_data = False
			config_data = False

def everypool():
	allpools()
	return {'pool': table}

if __name__ == "__main__":
	allpools()
	print(table)