from datetime import time
from typing import Tuple

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