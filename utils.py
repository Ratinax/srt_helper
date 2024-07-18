from Subtitle import Subtitle
import os
from times import get_time
import logs
import readline
from typing import List

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

def load_subtitiles(filename: str) -> List[Subtitle]:
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

def get_input(message, help_type: str = "", lower = False, disable_checker: bool = False):
	s = str(input(message))

	s = s.strip()
	skip = False
	if not disable_checker:
		args = s.split(' ')
		if args[0] == 'help':
			if len(args) > 1:
				logs.help_command(args[1])
			else:
				logs.help(help_type)
			skip = True
		if args[0] == 'clear':
			logs.clear()
			skip = True
	if lower:
		s = s.lower()
	return s, skip

def to_good_timestamp_format(timestamp: str):
	timestamp = timestamp.replace('.', ',')
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
