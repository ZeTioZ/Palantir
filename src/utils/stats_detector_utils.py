import pyautogui
import pytesseract
from PIL.Image import Resampling


def get_stats() -> list:
	"""
	Get the stats of the player in the game
	HUD Scale: 125%

	:return: a list containing the stats of the player in the game with the following format:
			[Wood, Food, Gold, Stone, Population]
			The population has the following format: "current/max"
	"""
	screenshot = pyautogui.screenshot()
	stats: list[None | str] = [None] * 5
	for i in range(0, 5):
		screenshot_cropped = screenshot.crop(((125 * i) + 65, 20, (125 * i) + 132, 50))
		screenshot_cropped = screenshot_cropped.resize((screenshot_cropped.width * 4, screenshot_cropped.height * 4), Resampling.LANCZOS)
		screenshot_cropped = screenshot_cropped.convert('L')
		screenshot_cropped = screenshot_cropped.point(lambda x: 0 if x < 150 else 255, '1')
		screenshot_cropped = screenshot_cropped.point(lambda x: 0 if x == 255 else 255, '1')
		screenshot_cropped = screenshot_cropped.convert('RGB')
		stats[i] = pytesseract.image_to_string(screenshot_cropped, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/").replace("\n", "").replace(" ", "").replace("O", "0")
		if i == 4 and stats[i].split("/")[0] == "":
			stats[i] = stats[i] = pytesseract.image_to_string(screenshot_cropped, config="--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789/").replace("\n", "").replace(" ", "").replace("O", "0")
	assert isinstance(stats, list), "stats should be a list"
	assert len(stats) == 5, "stats should be a list of length 5"
	for stat in stats:
		assert isinstance(stat, str), "each item in the stats list should be a string"
	return stats


def get_villagers_count() -> str:
	"""
	Get the stats about villagers of the player in the game
	HUD Scale: 125%

	:return: an integer containing the number of villagers of the player in the game
	"""
	screenshot = pyautogui.screenshot()
	screenshot_cropped = screenshot.crop(((125 * 4) + 20, 46, (125 * 4) + 61, 61))
	screenshot_cropped = screenshot_cropped.resize((screenshot_cropped.width * 4, screenshot_cropped.height * 4), Resampling.LANCZOS)
	screenshot_cropped = screenshot_cropped.convert('L')
	screenshot_cropped = screenshot_cropped.point(lambda x: 0 if x < 150 else 255, '1')
	screenshot_cropped = screenshot_cropped.point(lambda x: 0 if x == 255 else 255, '1')
	screenshot_cropped = screenshot_cropped.convert('RGB')
	villagers = pytesseract.image_to_string(screenshot_cropped, config="--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789").replace("\n", "").replace("O", "0")
	if villagers.strip() == "" or villagers is None:
		villagers = pytesseract.image_to_string(screenshot_cropped, config="--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789").replace("\n", "").replace("O", "0")
	assert isinstance(villagers, str), "villagers should be a string"
	return villagers


def get_actual_age() -> str:
	"""
	Get the actual age of the player in the game
	HUD Scale: 125%

	:return: a string containing the actual age of the player in the game
	"""
	screenshot = pyautogui.screenshot()
	screenshot_cropped = screenshot.crop((800, 20, 1010, 50))  # 125% HUD
	screenshot_cropped = screenshot_cropped.convert('L')
	age = pytesseract.image_to_string(screenshot_cropped, config="--psm 7 --oem 3").replace("\n", "").replace("O", "0").replace("’", "").strip()
	assert isinstance(age, str), "age should be a string"
	return age
