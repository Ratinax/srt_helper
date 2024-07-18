from utils import load_subtitiles, get_input
import os
import logs

def add_filename_copy(filename: str, filename_copy: str):
	if not os.path.exists(filename) or os.path.isdir(filename):
		logs.error(f'enter a valid file name')
	if os.path.exists(filename_copy) and os.path.isdir(filename_copy):
		logs.error(f'{filename_copy} is a directory')

	subtitles = load_subtitiles(filename)
	s, skip = get_input(f'\nYou are about to enter new texts for {filename} {len(subtitles)} subtitles and put them in {filename_copy} are you ready ? [y/n] ', lower=bool, disable_checker=True)
	if s == 'n':
		return
	for subtitle in subtitles:
		print(f'Enter new text for subtitle :\n{str(subtitle)[:-1]}')
		s, skip = get_input('Text : ', disable_checker=True)
		subtitle.text = s

	with open(filename_copy, 'w') as f_out:
		for subtitle in subtitles:
			f_out.write(str(subtitle))
	logs.successfully_copied(filename, filename_copy, len(subtitles))