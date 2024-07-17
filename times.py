from datetime import datetime, time, timedelta

def get_time(time_string: str):
	datetime_obj = datetime.strptime(time_string, '%H:%M:%S,%f')

	time_obj = datetime_obj.time()
	return time_obj

def add_time(initial_time: time, time_to_add: timedelta):
	datetime_obj = datetime.combine(datetime.min, initial_time)

	new_datetime_obj = datetime_obj + time_to_add

	new_time_obj = new_datetime_obj.time()

	return new_time_obj