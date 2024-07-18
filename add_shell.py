import os
import logs
from utils import load_subtitiles, get_input, get_pre_sub, to_good_timestamp_format
from Subtitle import Subtitle
from datetime import time, timedelta
from times import add_time, get_time
from typing import Tuple
from delete_ids import delete_subtitle

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


def get_timestamps_duration(subtitles: list, id: int = -1):
	s = None
	while s is None:
		s, skip = get_input('Enter duration: ', 'duration')
		if skip:
			s = None
			continue
		try:
			s = s.replace(',', '.')
			duration = float(s)
		except:
			s = None
			logs.error('wrong duration format, enter help for more infos')
	timestamp = get_pre_sub_timestamp(subtitles, id)
	return [timestamp, add_time(timestamp, timedelta(seconds=duration))]

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


def add_filename(filename: str):
	if os.path.exists(filename) and os.path.isdir(filename):
		logs.error('You should not enter a directory as filename')
		return

	subtitles = load_subtitiles(filename)
	file = open(filename, 'a')
	while True:
		# Get timestamps of new subtitle
		s, skip = get_input("Enter timestamps or duration ? ([0|t]/[1|d]/q/r) : ", 'timestamp_or_duration', lower=True)
		if skip: continue
		if s in '0tT1dD':
			if s in '0tT':
				timestamps = get_timestamps_timestamps(subtitles)
			elif s in '1dD':
				timestamps = get_timestamps_duration(subtitles)
			timestamps = get_timestamps_based_partial(subtitles, timestamps)
		elif s == 'r':
			if len(subtitles) == 0:
				logs.error('cannot remove non-existing subtitles')
				continue
			sub_removed: Subtitle = subtitles.pop(-1)
			file.close()
			delete_subtitle(filename, [str(sub_removed.id)])
			file = open(filename, 'a')
			continue
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
