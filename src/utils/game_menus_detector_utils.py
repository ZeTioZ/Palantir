import cv2
import numpy as np
import pyautogui
from pytesseract import pytesseract


def is_on_team_selection_screen() -> bool:
	"""
	:return: a boolean indicating if we are on the team selection screen
	"""
	screenshot = pyautogui.screenshot()
	randomize_text = screenshot.crop((1250, 985, 1355, 1005))
	assert isinstance(pytesseract.image_to_string(randomize_text, config="--psm 7 --oem 3"), str), "Image to string conversion failed."
	return pytesseract.image_to_string(randomize_text, config="--psm 7 --oem 3").replace("\n", "").lower() == "randomize"


def is_on_civilization_selection_screen() -> bool:
	"""
	:return: a boolean indicating if we are on the civilization selection screen
	"""
	screenshot = pyautogui.screenshot()
	confirm_text = screenshot.crop((745, 45, 1180, 90))
	assert isinstance(pytesseract.image_to_string(confirm_text, config="--psm 7 --oem 3"), str), "Image to string conversion failed."
	return pytesseract.image_to_string(confirm_text, config="--psm 7 --oem 3").replace("\n", "").lower() == "select civilization"


def is_on_game_start_screen() -> bool:
	"""
	:return: a boolean indicating if we are on the game start screen
	"""
	splash_screen = cv2.imread("./resources/images/game_start_splash.png")
	splash_screen_gray = cv2.cvtColor(splash_screen, cv2.COLOR_BGR2GRAY)
	screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
	found = cv2.matchTemplate(screenshot, splash_screen_gray, cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	assert isinstance(splash_screen, np.ndarray), "Game start splash image could not be loaded."
	assert isinstance(splash_screen_gray, np.ndarray), "Image conversion failed."
	assert isinstance(screenshot, np.ndarray), "Screenshot could not be taken."
	assert isinstance(found, np.ndarray), "Template matching failed."
	return bool(np.max(found >= threshold))


def is_on_in_game_screen() -> bool:
	"""
	:return: a boolean indicating if we are on the in game screen
	"""
	result = [False] * 2
	for i in range(2):
		in_game_template = cv2.imread(f"./resources/images/in_game_template_{i}.png")
		in_game_template_gray = cv2.cvtColor(in_game_template, cv2.COLOR_BGR2GRAY)
		screenshot = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_BGR2GRAY)
		found = cv2.matchTemplate(screenshot, in_game_template_gray, cv2.TM_CCOEFF_NORMED)
		threshold = 0.8
		result[i] = bool(np.max(found >= threshold))
	assert isinstance(result, list), "Result should be a list."
	for r in result:
		assert isinstance(r, bool), "Result should be a list of booleans."
	return any(result)
