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

def help_command(command: str = ""):
	print()
	if command == "add":
		print('usage: add [filename]')
		print('used to add subtitles one by one in a file')
	elif command == "add_copy":
		print('add_copy [filename] [other_filename]')
		print('used to copy the timestamps and the order of subtitles in another file and change them')
		print('(usually used to make multiple languages subtitiles simpler)')
	elif command == "clear":
		print('clear')
		print('used to clear the terminal')
	elif command == "help":
		print('help [optionnal command]')
		print('used to display current help or command help')
	elif command == "delete":
		print('delete [filename] [id1,id2,id3]')
		print('used to remove specific subtitles from a file')
	elif command == "delete_time":
		print('delete_time [filename] [timestamp1] [optionnal timestamp2]')
		print('used to delete all subtitles that are between first and second timestamp')
		print('if second timestamp is not providied, it will delete all subtitles after first timestamp')
	elif command in ["quit", "exit", "q"]:
		print("quit|exit|q")
		print("used to leave the program")
	print()

def help(path: str = ""):
	print()
	if path == "":
		print('Command list: ')
		print('    add [filename]')
		print('    add_copy [filename] [other_filename]')
		print('    delete [filename] [id1,id2,id3...]')
		print('    delete_time [filename] [timestamp1] [optionnal timestamp2]')
		print('    clear')
		print('    help [optionnal command]')
		print('    quit|exit|q')
	elif path == "timestamp_or_duration":
		print('duration in seconds and/or microseconds SS,MMM')
		print('example: 755,215 for 755 seconds and 215 microseconds')
		print('timestamp format: HH:MM:SS,MMM (can ommit infos)')
		print('examples: ')
		print('    05:00:12 for 5 hours 0 minutes, 12 seconds and 0 ms')
		print('    12,1 for the next timestamp possible with 12 seconds and 100 microseconds')
		print('Enter q if you want to quit')
		print('Enter r if you want to remove the last subtitle you provided')
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

def successfully_copied(filename, filename_copy, subtitles_amount):
	print(f'\n{GREEN}Successfully copy {filename} {subtitles_amount} subtitles with new ones in {filename_copy} !{RESET}\n')

def clear():
	lines = os.get_terminal_size().lines
	for i in range(lines):
		sys.stdout.write('\n')
	for i in range(lines):
		sys.stdout.write("\033[F")