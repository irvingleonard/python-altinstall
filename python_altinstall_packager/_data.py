#!python
"""

"""

from json import loads as json_loads
from logging import getLogger
from pathlib import Path
from sys import modules

LOGGER = getLogger(__name__)

def __getattr__(name):
	"""
	
	:param name:
	:return:
	"""
	
	file_path = Path(__file__).parent / 'data' / (name + '.json')
	if not file_path.exists():
		raise AttributeError(name)
	
	value = json_loads(file_path.read_text())
	setattr(modules[__name__], name, value)
	return value
