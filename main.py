import sys
import logs
import os
from datetime import datetime, timedelta, time
from typing import Tuple
from times import *
import readline

class Subtitle:
	def __init__(self, id: int = 0, timestamps: Tuple[time, time] = [], text: str = '') -> None:
		self.id = id
		self.timestamps = timestamps
		self.text = text
	def __str__(self):
		return (f'{self.id}\n'
				f'{self.timestamps[0].strftime('%H:%M:%S,%f')[:-3]}'
				f' --> '
				f'{self.timestamps[1].strftime('%H:%M:%S,%f')[:-3]}\n'
				f'{self.text}\n\n'
				)

def get_input(message, help_type: str = "", lower = False, disable_checker: bool = False):
	s = str(input(message))

	s = s.strip()
	skip = False
	if not disable_checker:
		if s == 'help':
			logs.help(help_type)
			skip = True
		if s == 'clear':
			logs.clear()
			skip = True
	if lower:
		s = s.lower()
	return s, skip

def get_pre_sub(subtitles: list, id: int = -1) -> Subtitle:
	sub = None

	if id == -1:
		max_id = -1
		for subtitle in subtitles:
			if max_id < subtitle.id:
				max_id = subtitle.id
				sub = subtitle
	else:
		for subtitle in subtitles:
			if subtitle.id == id - 1:
				sub = subtitle
				break
	return sub

def get_max_id(subtitles: list):
	sub = get_pre_sub(subtitles)

	if sub is None:
		return 0
	return sub.id + 1

def get_pre_sub_timestamp(subtitles: list, id: int = -1):
	sub = get_pre_sub(subtitles, id)

	if sub is None:
		return time()
	return sub.timestamps[1]

def to_good_timestamp_format(timestamp: str):
	# add microseconds
	sp = timestamp.split(',')
	if len(sp) == 1:
		timestamp = timestamp + ',0'

	# add seconds
	elif len(sp) == 2 and sp[0] == '':
		timestamp = '00' + timestamp

	# add : for minutes and hours missing
	sp = timestamp.split(':')
	for _ in range(3 - len(sp)):
		timestamp = ':' + timestamp

	# add hours and minutes
	sp = timestamp.split(':')
	timestamp = sp[-1]
	for i in range(1, -1, -1):
		if sp[i] == '':
			sp[i] = '00'
		timestamp = sp[i] + ':' + timestamp

	return timestamp

def get_timestamps_duration(subtitles: list, id: int = -1):
	s = None
	while s is None:
		s, skip = get_input('Enter duration: ', 'duration')
		if skip:
			s = None
			continue
		try:
			duration = float(s)
		except:
			s = None
			logs.error('wrong duration format, enter help for more infos')
	timestamp = get_pre_sub_timestamp(subtitles, id)
	return timestamp, add_time(timestamp, timedelta(seconds=duration))

def get_timestamps_timestamps(subtitles: list, id: int = -1):
	timestamps = []

	s = None
	while s is None:
		s, skip = get_input('Enter 1st timestamp: ', 'timestamps')
		if skip:
			s = None
			continue
		if s == '':
			timestamp = get_pre_sub_timestamp(subtitles, id)
			timestamps.append(timestamp)
		else:
			try:
				s = to_good_timestamp_format(s)
				time_obj = get_time(s)
				timestamps.append(time_obj)
			except:
				s = None
				logs.error('wrong timestamp format, enter help for more infos')

	s = None
	while s is None:
		s, skip = get_input('Enter 2nde timestamp: ', 'timestamps')
		if skip:
			s = None
			continue
		try:
			s = to_good_timestamp_format(s)
			time_obj = get_time(s)
			timestamps.append(time_obj)
		except:
			s = None
			logs.error('wrong timestamp format, enter help for more infos')

	return timestamps.copy()

def get_timestamp_based_partial(partial_timestamp: time, timestamp: time, is_second_timestamp = False):
	tmp_timestamp = timestamp

	if partial_timestamp.microsecond:
		tmp_timestamp = tmp_timestamp.replace(microsecond = partial_timestamp.microsecond)
	if partial_timestamp.second:
		tmp_timestamp = tmp_timestamp.replace(second = partial_timestamp.second)
	if partial_timestamp.minute:
		tmp_timestamp = tmp_timestamp.replace(minute = partial_timestamp.minute)
	if partial_timestamp.hour:
		tmp_timestamp = tmp_timestamp.replace(hour= partial_timestamp.hour)

	if is_second_timestamp and tmp_timestamp <= timestamp \
		or not is_second_timestamp and tmp_timestamp < timestamp:
		if partial_timestamp.hour:
			tmp_timestamp = tmp_timestamp.replace(hour=tmp_timestamp.hour + 1)
		elif partial_timestamp.minute:
			tmp_timestamp = tmp_timestamp.replace(hour=tmp_timestamp.hour + 1)
		elif partial_timestamp.second:
			tmp_timestamp = tmp_timestamp.replace(minute=tmp_timestamp.minute + 1)
		elif partial_timestamp.microsecond:
			tmp_timestamp = tmp_timestamp.replace(second=tmp_timestamp.second + 1)

	return tmp_timestamp

def get_timestamps_based_partial(subtitles: list, timestamps: Tuple[time, time], id: int = -1):
	new_timestamps = []
	timestamp = get_pre_sub_timestamp(subtitles, id)

	new_timestamps.append(get_timestamp_based_partial(timestamps[0], timestamp))
	timestamps[0] = new_timestamps[0]
	new_timestamps.append(get_timestamp_based_partial(timestamps[1], timestamps[0], True))

	return new_timestamps.copy()

def load_subtitiles(filename: str):
	subtitles = []
	if not os.path.exists(filename):
		return subtitles
	file = open(filename, 'r')
	i = 1
	subtitle = Subtitle()
	for line in file:
		line = line[:-1]
		# Id line
		if i % 4 == 1:
			subtitle.id = int(line)
		# timestamps line
		elif i % 4 == 2:
			subtitle.timestamps = [get_time(time_string) for time_string in line.split(' --> ')]
		# Text line
		elif i % 4 == 3:
			subtitle.text = line
		# Empty line
		elif i % 4 == 0:
			subtitles.append(subtitle)
			subtitle = Subtitle()
		i += 1
	file.close()
	return subtitles

def add_filename(filename: str):
	if os.path.exists(filename) and os.path.isdir(filename):
		logs.error('You should not enter a directory as filename')
		return

	subtitles = load_subtitiles(filename)
	file = open(filename, 'a')
	while True:
		# Get timestamps of new subtitle
		s, skip = get_input("Enter timestamps or duration ? ([0|t]/[1|d]/[q]) : ", 'timestamp_or_duration', lower=True)
		if skip: continue
		if s in '0tT1dD':
			if s in '0tT':
				timestamps = get_timestamps_timestamps(subtitles)
			elif s in '1dD':
				timestamps = get_timestamps_duration(subtitles)
			timestamps = get_timestamps_based_partial(subtitles, timestamps)
		elif s.lower() in ['q', 'quit', 'exit']:
			file.close()
			return
		else:
			logs.error('should enter one of the following chars : 0tT1dD')

		# Get text of new subtitle
		s, skip = get_input("Enter text : ", disable_checker=True)
		text = s

		# Get id of new subtitle
		id = get_max_id(subtitles)

		subtitle = Subtitle(id, timestamps, text)
		subtitles.append(subtitle)
		file.write(str(subtitle))

		logs.successfully_added(subtitle)

		# Update file in real time for user
		file.close()
		file = open(filename, 'a')

def delete_subtitle(filename: str, ids: str | list):
	if not os.path.exists(filename) or os.path.isdir(filename):
		logs.error('You should enter a valid filename')
		return
	lines = []
	ids_found = []
	with open(filename, 'r') as f_in:
		i = 1
		found = False
		for line in f_in:
			if i % 4 == 1 and line[:-1] in ids:
				ids_found.append(line[:-1])
				found = True
			if not found:
				lines.append(line)
			if i % 4 == 0:
				found = False
			i += 1

	ids_not_found = []
	for id in ids:
		if id not in ids_found:
			ids_not_found.append(id)

	if len(ids_not_found) > 0:
		logs.warning(f'Ids {ids_not_found} not found')

	logs.successfully_deleted(len(ids_found))

	with open(filename, 'w') as f_out:
		for line in lines:
			f_out.write(line)

def get_timestamp_ids(filename: str, timestamp1: str, timestamp2: str):
	timestamp1 = to_good_timestamp_format(timestamp1)
	timestamp2 = to_good_timestamp_format(timestamp2)
	timestamp_start = get_time(timestamp1)
	timestamp_end = get_time(timestamp2)

	subtitles: list[Subtitle] = load_subtitiles(filename)
	ids = []
	for subtitle in subtitles:
		if subtitle.timestamps[0] >= timestamp_start \
			and subtitle.timestamps[0] <= timestamp_end \
			and subtitle.timestamps[1] >= timestamp_start \
			and subtitle.timestamps[1] <= timestamp_end:
			ids.append(str(subtitle.id))
	return ids


logs.clear()

while True:
	s, skip = get_input('srt_helper$ ', lower=True)
	if skip: continue
	args = s.split(' ')
	if args[0] == 'add':
		if len(args) > 1:
			add_filename(args[-1])
		else:
			logs.error('add usage: add [filename]')
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
			args.append('999999999:999999999:999999999,000')
		ids_to_remove = get_timestamp_ids(args[1], args[2], args[3])
		delete_subtitle(args[1], ids_to_remove)
	elif s != '' and args[0] in ['quit', 'exit', 'q']:
		break
	elif s == '':
		continue
	else:
		logs.error(f'{s.split(' ')[0]}: command not found')