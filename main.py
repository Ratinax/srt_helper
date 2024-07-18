import sys
import logs
import os
from datetime import datetime, timedelta, time
from typing import Tuple
from times import *
from add_shell import add_filename
from utils import get_input
from delete_ids import delete_subtitle, get_timestamp_ids
from add_copy_shell import add_filename_copy

logs.clear()
print('Welcome in srt helper, a tool to help you build srt files')
print('If you want some help just type help')
print()

while True:
	s, skip = get_input('srt_helper$ ', lower=True)
	if skip: continue
	args = s.split(' ')
	if args[0] == 'add':
		if len(args) == 2:
			add_filename(args[1])
		else:
			logs.error('add usage: add [filename]')
	elif args[0] == 'add_copy':
		if len(args) == 3:
			add_filename_copy(args[1], args[2])
		else:
			logs.error('add_copy usage: add_copy [filename] [other_filename]')
	elif args[0] == 'delete':
		if len(args) != 3:
			logs.error('delete usage: delete [filename] [id]')
			continue
		delete_subtitle(args[1], args[2].split(','))
	elif args[0] == 'delete_time':
		args = s.split(' ')
		if len(args) not in [3, 4]:
			logs.error('delete_time usage: delete_time [filename] [timestamp1] [optionnal timestamp2]')
			continue
		if len(args) == 3:
			args.append('23:59:59,000')
		ids_to_remove = get_timestamp_ids(args[1], args[2], args[3])
		delete_subtitle(args[1], ids_to_remove)
	elif s != '' and args[0] in ['quit', 'exit', 'q']:
		break
	elif s == '':
		continue
	else:
		logs.error(f'{s.split(' ')[0]}: command not found')