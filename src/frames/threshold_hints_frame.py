import wx

from utils.startegies_parser_utils import get_civilization_strategy
from utils.stats_detector_utils import get_stats, get_villagers_count, get_actual_age


class ThresholdHintsFrame(wx.Frame):
	"""
	The thresholds hints frame.
	It is a child of the in game screen frame and is only visible when the game is in focus and the thresholds are triggered.
	"""
	def __init__(self, parent, title):
		super(ThresholdHintsFrame, self).__init__(parent, title=title, size=(200, 75))
		assert isinstance(parent, wx.Frame), "parent must be an instance of wx.Frame class"
		self.parent = parent
		self.SetPosition((800, 70))
		self.SetWindowStyle(
			wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.FRAME_TOOL_WINDOW | wx.TRANSPARENT_WINDOW)
		self.SetTransparent(210)
		self.SetBackgroundColour((255, 255, 0))
		self.Bind(wx.EVT_TIMER, self.update, id=1)
		self.updateTimer = wx.Timer(self, 1)
		self.updateTimer.Start(1000)
		self.Show(False)

		self.best_pick_cache = None
		self.players_number_cache = 0

		self.font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

		self.description_name_label = wx.StaticText(self, label="", style=wx.ALIGN_LEFT)
		self.description_name_label.SetFont(self.font)
		self.description_name_label.Wrap(184)
		self.description_name_label.SetPosition((8, (self.description_name_label.GetSize()[1] // 2)))

	def update(self, event):
		"""
		Update the frame. The updates are tied to a timer that fires every second.
		:param event: the timer event.
		"""
		if self.parent.IsShown():
			show = False
			player_stats_cache = get_stats()
			player_villagers_count_cache = get_villagers_count()
			player_villagers_count_cache = player_villagers_count_cache if player_villagers_count_cache != "" else 0
			player_actual_age_cache = get_actual_age().replace(" ", "_").lower()
			strategy_cache = get_civilization_strategy(self.parent.parent.player_civilization)
			if self.parent.parent.player_civilization is not None and \
					player_stats_cache is not None and \
					player_villagers_count_cache is not None and \
					player_actual_age_cache is not None and \
					strategy_cache is not None and \
					player_actual_age_cache in ["dark_age", "feudal_age", "castle_age", "imperial_age"]:
				gold_treshold = int(strategy_cache["thresh_holds"]["gold"][player_actual_age_cache])
				food_treshold = int(strategy_cache["thresh_holds"]["food"][player_actual_age_cache])
				wood_treshold = int(strategy_cache["thresh_holds"]["wood"][player_actual_age_cache])
				stone_treshold = int(strategy_cache["thresh_holds"]["stone"][player_actual_age_cache])
				villagers_treshold = int(strategy_cache["thresh_holds"]["villagers"][player_actual_age_cache])
				if int(player_stats_cache[2]) > gold_treshold and \
						int(player_stats_cache[1]) > food_treshold and \
						int(player_stats_cache[0]) > wood_treshold and \
						int(player_stats_cache[3]) > stone_treshold:
					self.description_name_label.SetLabel("Enough resources to upgrade your town center to the next age!")
					show = True
				elif int(player_villagers_count_cache) > villagers_treshold:
					self.description_name_label.SetLabel("You have enough villagers! Start to create some army units!")
					show = True
				self.Show(show and self.parent.IsShown())
				self.description_name_label.Wrap(184)
		else:
			self.Show(False)
