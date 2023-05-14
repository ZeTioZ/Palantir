import time

from threading import Thread

import win32api
import win32con


class KeyPressThread(Thread):

	key_pressed: float = 0

	def __init__(self, attached_frame):
		"""
		Thread that checks if the left mouse button is pressed.
		"""
		super().__init__()
		self.daemon = True
		self.attached_frame = attached_frame
		self.cancel = False

	def run(self):
		"""
		Checks if the left mouse button is pressed and if it is, it will check if the mouse is over a button
		and if it is, it will call the button's function.
		"""
		while True:
			if win32api.GetKeyState(win32con.VK_LBUTTON) < 0 and not self.is_key_on_cooldown():
				self.key_pressed = time.time() + 0.1
				for(button, function) in self.attached_frame.buttons.items():
					if self.HitTest(button, win32api.GetCursorPos()):
						function()
			if self.cancel:
				break

	def is_key_on_cooldown(self) -> bool:
		"""
		Checks if the key press is on cooldown.
		:return: True if the key press is on cooldown, False otherwise.
		"""
		return not self.key_pressed < time.time()

	def stop(self):
		"""
		Stops the thread.
		"""
		self.cancel = True

	@staticmethod
	def HitTest(button, point):
		"""
		Checks if the mouse is inside a button by checking if the mouse's position is inside the button's rectangle.
		:param button: Button to check.
		:param point: Mouse's position.
		:return: True if the mouse is inside the button, False otherwise.
		"""
		button_position = button.GetScreenPosition()
		button_size = button.GetSize()
		button_x1 = button_position[0]
		button_x2 = button_position[0] + button_size[0]
		button_y1 = button_position[1]
		button_y2 = button_position[1] + button_size[1]
		return button_x1 < point[0] < button_x2 and button_y1 < point[1] < button_y2
