from threading import Thread
from utils.process_utils import is_process_running


class AutoCloseThread(Thread):
	"""
	Thread that closes the application when the game is closed.
	"""
	def __init__(self):
		super().__init__()
		self.daemon = True
		self.close = False

	def run(self):
		"""
		Checks if the game is running.
		"""
		self.close = not is_process_running('AoE2DE_s.exe')
