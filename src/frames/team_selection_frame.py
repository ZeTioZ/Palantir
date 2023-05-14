import wx

from utils.startegies_parser_utils import get_civilization_strategy
from utils.team_detector_utils import get_best_pick, get_players_amount


class TeamSelectionFrame(wx.Frame):
	"""
	Frame that shows the best counter pick for the current civilization selection.
	It is a child of the main frame and is only visible when the game is in focus and the player is on the right screen.
	"""
	def __init__(self, parent, title):
		super(TeamSelectionFrame, self).__init__(parent, title=title, size=(500, 250))
		self.parent = parent
		self.SetPosition((1370, 50))
		self.SetWindowStyle(
			wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.FRAME_TOOL_WINDOW | wx.TRANSPARENT_WINDOW)
		self.SetTransparent(210)
		self.Show(True)

		self.best_pick_cache = None
		self.players_number_cache = 0

		self.font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

		title_text = "Best Counter Pick"
		self.title_text_label = wx.StaticText(self, label=title_text, style=wx.ALIGN_LEFT, pos=(170, 10))
		self.title_text_label.SetFont(self.font)

		civilization_name = "Civilization: Loading... Please wait..."
		self.civilization_name_label = wx.StaticText(self, label=civilization_name, style=wx.ALIGN_LEFT, pos=(10, 60))
		self.civilization_name_label.SetFont(self.font)

		strategies_name = "Specialities: Loading... Please wait..."
		self.strategies_name_label = wx.StaticText(self, label=strategies_name, style=wx.ALIGN_LEFT, pos=(10, 100))
		self.strategies_name_label.SetFont(self.font)

		description_name = "Description: Loading... Please wait..."
		self.description_name_label = wx.StaticText(self, label=description_name, style=wx.ALIGN_LEFT, pos=(10, 140))
		self.description_name_label.SetFont(self.font)
		self.description_name_label.Wrap(480)

	def update(self, is_on_team_selection_screen_cache, is_on_civilization_selection_screen_cache):
		"""
		Updates the frame with the best counter pick for the current civilization selection.
		The updates are tied to the main frame.
		:param is_on_team_selection_screen_cache: A cached boolean that indicates if the user is on the team selection screen.
		:param is_on_civilization_selection_screen_cache: A cached boolean that indicates if the user is on the civilization selection screen.
		:return:
		"""
		self.Show(self.parent.IsShown())
		if not is_on_civilization_selection_screen_cache and is_on_team_selection_screen_cache:
			best_pick = get_best_pick().strip()
			if len(best_pick) > 0 and best_pick != self.best_pick_cache and not is_on_civilization_selection_screen_cache:
				assert len(best_pick) > 0 and best_pick != self.best_pick_cache and not is_on_civilization_selection_screen_cache, "Something went wrong with the best pick selection"
				self.best_pick_cache = best_pick if best_pick != "" and best_pick != self.best_pick_cache else self.best_pick_cache
				strategy = get_civilization_strategy(best_pick)
				self.civilization_name_label.SetLabelText("Civilization: " + best_pick)
				self.strategies_name_label.SetLabelText(
					"Specialities: " + strategy["specialty"].replace("_", " ").capitalize())
				self.description_name_label.SetLabelText("Description: " + strategy["description"])
				self.description_name_label.Wrap(480)

			players_number = get_players_amount()
			if players_number != 0 and players_number != self.parent.players_number and is_on_team_selection_screen_cache:
				self.parent.players_number = players_number
