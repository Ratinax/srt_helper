import sys
import os

RED = "\033[31m"
RESET = "\033[0m"

def error(*args, **kwargs):
	print(f'{RED}Error:{RESET}', *args, **kwargs)

def help(path: str = ""):
	print()
	if path == "":
		print('Command list: ')
		print('    add [filename]')
		print('    modify [filename]')
		print('    otla [filename]')
		print('    clear')
	elif path == "timestamp_or_duration":
		print('duration in seconds and/or milliseconds SS,MMM')
		print('example: 755,215 for 755 seconds and 215 milliseconds')
		print('timestamp format: HH:MM:SS,MMM (can ommit infos)')
		print('examples: ')
		print('    05:00:12 for 5 hours 0 minutes, 12 seconds and 0 ms')
		print('    12,1 for the next timestamp possible with 12 seconds and 100 milliseconds')
	elif path == "duration":
		print('duration in seconds and/or milliseconds SS,MMM')
		print('examples:')
		print('    755,215 for 755 seconds and 215 milliseconds')
		print('    5 for 5 seconds')
		print('    ,5 for 500 ms')
	elif path == "timestamps":
		print('timestamp format: HH:MM:SS,MMM (can ommit infos)')
		print('examples: ')
		print('    05:00:12 for 5 hours 0 minutes, 12 seconds and 0 ms')
		print('    12,1 for the next timestamp possible with 12 seconds and 100 milliseconds')
		print('    5:10 for the next timestamp possible with 5 minutes and 10 seconds')
		print('you may also just hit Enter if it\'s the first to be entered, it would automatically put a good timestamp')
	print()


def clear():
	lines = os.get_terminal_size().lines
	for i in range(lines):
		sys.stdout.write('\n')
	for i in range(lines):
		sys.stdout.write("\033[F")