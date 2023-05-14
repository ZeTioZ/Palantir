import wx

from frames import threshold_hints_frame
from threads.key_press_thread import KeyPressThread
from utils.startegies_parser_utils import get_civilization_strategy
from utils.stats_detector_utils import get_actual_age
from utils.team_detector_utils import get_player_team_in_game


class InGameScreenFrame(wx.Frame):
	"""
	The in game screen frame.
	It is a child of the main frame and is only visible when the game is in focus and the player is on the right screen.
	"""
	def __init__(self, parent, title):
		super(InGameScreenFrame, self).__init__(parent, -1, title=title, size=(500, 250))
		self.parent = parent
		self.SetPosition((1370, 125))
		self.SetWindowStyle(wx.STAY_ON_TOP | wx.FRAME_SHAPED | wx.FRAME_TOOL_WINDOW | wx.BORDER_NONE | wx.TRANSPARENT_WINDOW)
		self.SetTransparent(210)
		self.Show(True)

		self.key_press_thread = KeyPressThread(self)
		self.key_press_thread.start()

		self.hint_frame = threshold_hints_frame.ThresholdHintsFrame(self, "Thresholds")

		self.actual_age_cache = ""
		self.actual_page = 0
		self.strategy_cache = []

		self.button_left_button = wx.Button(self, label="<")
		self.button_left_button.SetPosition((8, 100))
		self.button_left_button.SetSize((50, 50))
		self.button_left_button.Bind(wx.EVT_LEFT_DOWN, self.on_left_button)
		self.button_left_button.Show(False)

		self.button_right_button = wx.Button(self, label=">")
		self.button_right_button.SetPosition((440, 100))
		self.button_right_button.SetSize((50, 50))
		self.button_right_button.Bind(wx.EVT_LEFT_DOWN, self.on_right_button)

		self.buttons = {self.button_left_button: self.on_left_button, self.button_right_button: self.on_right_button}

		main_sizer = wx.BoxSizer(wx.VERTICAL)
		age_sizer = wx.BoxSizer(wx.HORIZONTAL)
		text_sizer = wx.BoxSizer(wx.HORIZONTAL)

		font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
		self.actual_age_text = wx.StaticText(self, label="Loading... Please wait...", style=wx.ALIGN_CENTER)
		self.actual_age_text.SetFont(font)

		self.strategy_text = wx.StaticText(self, label="Loading the strategy... Please wait...", style=wx.ALIGN_CENTER)
		self.strategy_text.SetFont(font)
		self.strategy_text_width = 360
		self.strategy_text.Wrap(self.strategy_text_width)

		age_sizer.AddStretchSpacer()
		age_sizer.Add(self.actual_age_text, 0, wx.ALIGN_LEFT)
		age_sizer.AddStretchSpacer()
		text_sizer.AddSpacer(75)
		text_sizer.Add(self.strategy_text, 0, wx.ALIGN_LEFT)

		main_sizer.Add(age_sizer, -1, wx.EXPAND | wx.TOP, 10)
		main_sizer.Add(text_sizer, -1, wx.EXPAND | wx.TOP, -10)
		self.SetSizer(main_sizer)
		self.Layout()

	def on_left_button(self):
		"""
		When the left button is pressed, it will show the previous strategy page.
		"""
		if self.actual_page > 0:
			self.button_right_button.Show(True)
			self.actual_page -= 1
			assert self.actual_page >= 0, "The actual page can't be negative"
			self.strategy_text.SetLabel(f"{self.actual_page + 1}. {self.strategy_cache[self.actual_page]}")
			self.strategy_text.Wrap(self.strategy_text_width)
			if self.actual_page == 0:
				self.button_left_button.Show(False)

	def on_right_button(self):
		"""
		When the right button is pressed, it will show the next strategy page.
		"""
		if self.actual_page < len(self.strategy_cache) - 1:
			self.button_left_button.Show(True)
			self.actual_page += 1
			assert self.actual_page < len(self.strategy_cache), "The actual page can't be greater than the maximum page"
			self.strategy_text.SetLabel(f"{self.actual_page + 1}. {self.strategy_cache[self.actual_page]}")
			self.strategy_text.Wrap(self.strategy_text_width)
			if self.actual_page == len(self.strategy_cache) - 1:
				self.button_right_button.Show(False)

	def update(self, is_on_in_game_screen_cache):
		"""
		Updates the frame. The updates are tidied up with the main frame updates.
		:param is_on_in_game_screen_cache: The cache of the is_on_in_game_screen function coming from the main frame.
		"""
		actual_age = get_actual_age().replace(" ", "_").lower()
		self.Show(self.parent.IsShown() and is_on_in_game_screen_cache)
		if self.actual_age_cache != actual_age:
			self.actual_age_cache = actual_age
			self.actual_age_text.SetLabel(actual_age.replace("_", " ").title())
			self.actual_page = 0
			player_civilization = self.update_civ()
			temp_cache = get_civilization_strategy(player_civilization)
			if temp_cache is not None and actual_age in temp_cache.keys():
				self.strategy_cache = temp_cache[actual_age]
			if len(self.strategy_cache) > 0:
				self.strategy_text.SetLabel(f"{self.actual_page + 1}. {self.strategy_cache[self.actual_page]}")
				self.strategy_text.Wrap(self.strategy_text_width)

	def stop(self):
		"""
		Stops the key press thread.
		"""
		self.key_press_thread.stop()

	def update_civ(self):
		"""
		Updates the player civilization cache and returns it.
		:return: The player's newly cached civilization.
		"""
		self.parent.player_civilization = get_player_team_in_game()
		return self.parent.player_civilization
