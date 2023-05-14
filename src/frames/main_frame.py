import win32gui
import wx

from frames import team_selection_frame, in_game_screen_frame
from threads.auto_close_thread import AutoCloseThread
from utils.game_menus_detector_utils import *


class PalantirFrame(wx.Frame):
	"""
	The main frame of the application. It is the only frame that is always visible.
	Each sub-frame will be a child of this frame and register itself in the sub_frames_register.
	"""
	def __init__(self, parent, title):
		super(PalantirFrame, self).__init__(parent, title=title, size=(wx.GetDisplaySize()))
		self.SetWindowStyle(wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.FRAME_SHAPED | wx.FRAME_TOOL_WINDOW | wx.TRANSPARENT_WINDOW)
		self.Bind(wx.EVT_TIMER, self.update)
		self.SetTransparent(0)
		self.updateLoop = wx.Timer(self, 1)
		self.updateLoop.Start(20)
		self.autoCloseLoop = wx.Timer(self, 2)
		self.autoCloseLoop.Start(1000)
		self.sub_frames_register = dict()
		self.players_number = 0
		self.player_civilization = None
		self.Show(False)

	def update(self, event):
		"""
		Updates the main frame and the sub-frames. The main frame is only visible when the game is in focus.
		The sub-frames are only visible when the game is in focus and the player is on the right screen.
		The main frame is closed when the game process is not running anymore which closes all sub-frames too.

		:param event: The event that triggered the update (a timer event).
		"""
		timer: wx.Timer = event.GetTimer()
		assert timer.GetId() in [1, 2], f"Invalid timer ID: {timer.GetId()}"
		if timer.GetId() == 1:
			self.Show(win32gui.GetForegroundWindow() == win32gui.FindWindow(None, 'Age of Empires II: Definitive Edition'))
			is_on_team_selection_screen_cache = is_on_team_selection_screen()
			is_on_civilization_selection_screen_cache = is_on_civilization_selection_screen()
			is_on_in_game_screen_cache = is_on_in_game_screen()
			if is_on_team_selection_screen_cache or is_on_civilization_selection_screen_cache:
				if 'team_selection' not in self.sub_frames_register:
					self.sub_frames_register['team_selection'] = team_selection_frame.TeamSelectionFrame(self, title='Palantir - Team Selection')
				else:
					self.sub_frames_register['team_selection'].update(is_on_team_selection_screen_cache, is_on_civilization_selection_screen_cache)
			elif is_on_in_game_screen_cache:
				if 'in_game' not in self.sub_frames_register:
					self.sub_frames_register['in_game'] = in_game_screen_frame.InGameScreenFrame(self, title='Palantir - In Game')
				else:
					self.sub_frames_register['in_game'].update(is_on_in_game_screen_cache)
			if not (is_on_team_selection_screen_cache or is_on_civilization_selection_screen_cache):
				if 'team_selection' in self.sub_frames_register:
					self.sub_frames_register['team_selection'].Close()
					self.sub_frames_register['team_selection'].Destroy()
					del self.sub_frames_register['team_selection']
			if not is_on_in_game_screen_cache:
				if 'in_game' in self.sub_frames_register:
					self.sub_frames_register['in_game'].stop()
					self.sub_frames_register['in_game'].Close()
					self.sub_frames_register['in_game'].Destroy()
					del self.sub_frames_register['in_game']
			for sub_frame in self.sub_frames_register.values():
				assert isinstance(sub_frame, (team_selection_frame.TeamSelectionFrame, in_game_screen_frame.InGameScreenFrame)), f"Invalid sub-frame type: {type(sub_frame)}"
		elif timer.GetId() == 2:
			auto_close_thread = AutoCloseThread()
			auto_close_thread.start()
			assert auto_close_thread.is_alive(), "AutoCloseThread is not running"
			auto_close_thread.join()
			if auto_close_thread.close:
				exit()
