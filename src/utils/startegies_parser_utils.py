import json


def parse_strategy_from_json_file(file_path="./resources/counters.json") -> dict:
	"""
	Parse the overall strategies from the json file

	:param file_path: the path to the json file
	:return: a dictionary containing the overall strategies (detailed strategies are in individual civilization json files)
	"""
	with open(file_path, 'r') as file:
		return json.load(file)


def get_civilization_counters(civilization_name: str) -> list:
	"""
	Get the counters of the given civilization

	:param civilization_name: the name of the civilization
	:return: a list containing the counters of the given civilization
	"""
	strategies = parse_strategy_from_json_file()
	return strategies[civilization_name]['counters']


def get_civilization_strategy(civilization_name: str) -> dict:
	"""
	Get the detailed strategy of the given civilization for each age and a brief description of the strategy

	:param civilization_name: the name of the civilization
	:return: a dictionary containing the detailed strategy of the given civilization.
			Format: {"description": "brief description", "age": ["strategy steps"]}
	"""
	with open(f"./resources/strategies/{civilization_name}.json", 'r') as file:
		return json.load(file)
