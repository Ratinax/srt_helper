import sys
import os

RED = "\033[31m"
GREEN = "\033[32m"
PURLE = "\033[35m"
RESET = "\033[0m"

def error(*args, **kwargs):
	print(f'{RED}Error:{RESET}', *args, **kwargs)

def warning(*args, **kwargs):
	print(f'{PURLE}Warning:{RESET}', *args, **kwargs)

def help(path: str = ""):
	print()
	if path == "":
		print('Command list: ')
		print('    add [filename]')
		print('    delete [filename] [id1,id2,id3...]')
		print('    delete_time [filename] [timestamp1] [optionnal timestamp2]')
		print('    clear')
		print('    help')
		print('    quit|exit|q')
	elif path == "timestamp_or_duration":
		print('duration in seconds and/or microseconds SS,MMM')
		print('example: 755,215 for 755 seconds and 215 microseconds')
		print('timestamp format: HH:MM:SS,MMM (can ommit infos)')
		print('examples: ')
		print('    05:00:12 for 5 hours 0 minutes, 12 seconds and 0 ms')
		print('    12,1 for the next timestamp possible with 12 seconds and 100 microseconds')
		print('Enter q if you want to quit')
	elif path == "duration":
		print('duration in seconds and/or microseconds SS,MMM')
		print('examples:')
		print('    755,215 for 755 seconds and 215 microseconds')
		print('    5 for 5 seconds')
		print('    ,5 for 500 ms')
	elif path == "timestamps":
		print('timestamp format: HH:MM:SS,MMM (can ommit infos)')
		print('examples: ')
		print('    05:00:12 for 5 hours 0 minutes, 12 seconds and 0 ms')
		print('    12,1 for the next timestamp possible with 12 seconds and 100 microseconds')
		print('    5:10 for the next timestamp possible with 5 minutes and 10 seconds')
		print('you may also just hit Enter if it\'s the first to be entered, it would automatically put a good timestamp')
	print()

def successfully_deleted(amount):
	print(f'\n{GREEN}Successfully deleted {amount} items !{RESET}\n')

def successfully_added(subtitle):
	print(f'\n{str(subtitle)}{GREEN}Successfully added !{RESET}\n')



def clear():
	lines = os.get_terminal_size().lines
	for i in range(lines):
		sys.stdout.write('\n')
	for i in range(lines):
		sys.stdout.write("\033[F")