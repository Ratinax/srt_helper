import sys
import logs
import os
from datetime import datetime, timedelta
from typing import Tuple

class Subtitle:
	def __init__(self, id: int, timestamps: Tuple[datetime, datetime], text: str) -> None:
		self.id = id
		self.timestamps = timestamps
		self.text = text

def get_input(message, help_type: str = "", disable_checker: bool = False):
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

def to_good_timestamp_format(timestamp: str):
	# add milliseconds
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
	sub = get_pre_sub(subtitles, id)
	if sub is None:
		return timedelta(0), timedelta(seconds=duration)
	return sub.timestamps[1], sub.timestamps[1] + timedelta(seconds=duration)

def get_timestamps_timestamps(subtitles: list, id: int = -1):
	timestamps = []

	s = None
	while s is None:
		s, skip = get_input('Enter 1st timestamp: ', 'timestamps')
		if skip:
			s = None
			continue
		if s == '':
			sub = get_pre_sub(subtitles, id)
			if sub is None:
				timestamp = timedelta(seconds=0)
			else:
				timestamp = sub.timestamps[1]

			timestamps.append(timestamp)
		else:
			try:
				s = to_good_timestamp_format(s)
				time_obj = datetime.strptime(s, '%H:%M:%S,%f')
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
			time_obj = datetime.strptime(s, '%H:%M:%S,%f')
			timestamps.append(time_obj)
		except:
			s = None
			logs.error('wrong timestamp format, enter help for more infos')

	return timestamps.copy()

def get_timestamp_based_partial(partial_timestamp: datetime, timestamp: datetime):


def get_timestamps_based_partial(subtitles: list, timestamps: Tuple[datetime, datetime], id: int = -1):
	new_timestamps = []
	sub = get_pre_sub(id)
	new_timestamps.append(get_timestamp_based_partial(timestamps[0], sub.timestamps[1]))
	new_timestamps.append(get_timestamp_based_partial(timestamps[1], timestamps[0]))


def add_filename(filename: str):
	if os.path.exists(filename) and os.path.isdir(filename):
		logs.error('You should not enter a directory as filename')
		return

	file = open(filename, 'a')
	subtitles = []
	while True:
		s, skip = get_input("Enter timestamps or duration ? ([0|t|T]/[1|d|D]) : ", 'timestamp_or_duration')
		if skip: continue
		if s in '0tT1dD':
			if s in '0tT':
				timestamps = get_timestamps_timestamps(subtitles)
			elif s in '1dD':
				timestamps = get_timestamps_duration(subtitles)
			timestamps = get_timestamps_based_partial(subtitles, timestamps)
		else:
			logs.error('should enter one of the following chars : 0tT1dD')


logs.clear()

while True:
	s, skip = get_input('srt_helper$ ')
	if skip: continue
	if s[:3] == 'add':
		if len(s.split(' ')) > 1:
			add_filename(s.split(' ')[-1])
		else:
			logs.error('add usage: add [filename]')