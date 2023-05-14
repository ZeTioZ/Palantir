import pyautogui
import pytesseract
import os
import cv2
import numpy as np

from utils.game_menus_detector_utils import is_on_team_selection_screen
from utils.startegies_parser_utils import parse_strategy_from_json_file


def get_menu_teams() -> list:
	"""
	Get the civilizations of the teams in the menu and if on the team selection screen

	:return: a list containing the civilizations of the teams in the menu and if on the team selection screen
	"""
	if is_on_team_selection_screen():
		screenshot = pyautogui.screenshot()
		civilizations = [None] * 8
		assert (len(civilizations) == 8)
		for i in range(0, 8):
			screenshot_cropped = screenshot.crop((860, (45 * i) + 375, 1025, (45 * i) + 405))
			civilizations[i] = pytesseract.image_to_string(screenshot_cropped).replace("\n", "")
		return civilizations


def get_player_team_in_game() -> str:
	"""
	:return: the team of the player while in game using the emblems on the top right of the screen
	"""
	directory: str = ".\\resources\\images\\emblems"
	methods = ['cv2.TM_CCORR_NORMED']
	for filename in os.listdir(directory):
		f = os.path.join(directory, filename)
		if os.path.isfile(f):
			cv_emblem = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
			screenshot = pyautogui.screenshot().crop((1520, 3, 1583, 66))
			screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
			for meth in methods:
				method = eval(meth)
				found = cv2.matchTemplate(screenshot, cv_emblem, method)
			threshold = 0.9
			if bool(np.max(found >= threshold)):
				return filename.replace(".png", "")


def get_players_amount() -> int:
	"""
	Get the amount of players in the game from the team selection screen

	:return: the amount of players in the game
	"""
	teams = get_menu_teams()
	if teams is None:
		return 0
	numbers = len(list(filter(lambda x: x != "" and not None, teams)))
	return numbers


# Useless since now we detect the team directly in game from the emblems
# def get_loading_screen_teams(players_number: int) -> list:
# 	screenshot = pyautogui.screenshot()
# 	players_number = players_number if players_number > 0 else 1
# 	civilizations = [None] * players_number
# 	assert (len(civilizations) == players_number)
# 	start_top_y = (560 if players_number % 2 != 0 else 600) - (players_number // 2) * 76
# 	start_bottom_y = (585 if players_number % 2 != 0 else 625) - (players_number // 2) * 76
# 	for i in range(0, players_number):
# 		screenshot_cropped = screenshot.crop((185, (76 * i) + start_top_y, 450, (76 * i) + start_bottom_y))
# 		civilizations[i] = pytesseract.image_to_string(screenshot_cropped).replace("\n", "")
# 	return civilizations


def get_counters():
	"""
	:return: a dictionary containing all the counters for each civilization
	"""
	result = dict()
	strategies = parse_strategy_from_json_file()
	for civilization in strategies.keys():
		result[civilization] = strategies[civilization]['counters']
	return result


def get_best_pick():
	"""
	:return: a string containing the best pick for the actual enemy selection
	"""
	teams = get_menu_teams()
	counters = get_counters()
	pick_dict = dict()
	if is_on_team_selection_screen():
		for team in teams[1:]:
			if team not in counters.keys():
				continue
			for counter in counters[team]:
				pick_dict = {counter: pick_dict.get(counter, 0) + 1}
	result = "" if len(pick_dict) == 0 else max(pick_dict, key=pick_dict.get)
	return result
