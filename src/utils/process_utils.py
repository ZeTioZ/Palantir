import psutil


def is_process_running(process_name):
	"""
	Check if there is any running process that contains the given process name.
	"""
	for proc in psutil.process_iter():
		try:
			if process_name.lower() in proc.name().lower():
				return True
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return False


def find_process_id_by_name(process_name):
	"""
	Get a list of all the PIDs of all the running process whose name contains
	the given process name
	"""
	list_of_process_objects = []
	for proc in psutil.process_iter():
		try:
			process_info = proc.as_dict(attrs=['pid', 'name'])
			if process_name.lower() in process_info['name'].lower():
				list_of_process_objects.append(process_info)
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return list_of_process_objects
