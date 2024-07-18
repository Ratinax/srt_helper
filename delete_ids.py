import os
import logs
from utils import to_good_timestamp_format, load_subtitiles
from times import get_time
from Subtitle import Subtitle

def delete_subtitle(filename: str, ids: list):
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
