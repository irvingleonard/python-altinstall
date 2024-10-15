#!python
"""

"""

from datetime import date as Date, datetime as Datetime
from logging import getLogger
from re import match as re_match

from semantic_version import Version as SemanticVersion

LOGGER = getLogger(__name__)


class Release(tuple):
	"""
	
	"""
	
	def __new__(cls, release, extra_stuff=None):
		"""

		:param args:
		:param kwargs:
		"""
		
		return super().__new__(cls, (release, extra_stuff))
	
	def __str__(self):
		"""
		
		:return:
		"""
		
		result = str(self[0])
		if self[1] is not None:
			result += str(self[1])
		return result
	
	@classmethod
	def from_str(cls, release_str):
		"""
		
		:param release_str:
		:return:
		"""
		
		result = re_match(r'^\s*(?P<release>\d+)(?P<extra_stuff>\D+)?\s*$', release_str)
		if result is None:
			raise ValueError("Couldn't parse the provided release: {}".format(release_str))
		result = result.groupdict()
		result['release'] = int(result['release'])
		return cls(**result)
	

class ChangelogEntry(tuple):
	"""
	
	"""
	
	DATE_FORMAT = r'%a %b %d %Y'
	ENTRY_FORMAT = r'^\s*(?P<entry_date>\S{3}\s+\S{3}\s+\d{1,2}\s+(?:\d{2}|\d{4}))\s+(?P<packager>.*?)(?:\s+\-)?\s+(?P<version>\S+?)\-(?P<release>\S+)\s*$'
	
	def __gt__(self, other):
		"""
		
		:param other:
		:return:
		"""

		if self.entry_date > other.entry_date:
			return True
		elif self.entry_date == other.entry_date:
			if self.version > other.version:
				return True
			elif (self.version == other.version) and (self.release > other.release):
				return True
			elif (self.version == other.version) and (self.release == other.release):
				return False
		elif self.version < other.version:
			return False
		elif (self.version == other.version) and (self.release < other.release):
			return False
		else:
			raise ValueError("Entries shouldn't be in the same changelog")
	
	def __lt__(self, other):
		"""
		
		:param other:
		:return:
		"""
		
		return other > self
	
	def __new__(cls, entry_date, packager, version, release):
		"""
		
		:param args:
		:param kwargs:
		"""
		
		return super().__new__(cls, (entry_date, packager, version, release))
	
	def __str__(self):
		"""
		
		:return:
		"""
		
		if hasattr(self[0], 'strftime'):
			entry_date = self[0].strftime(self.DATE_FORMAT)
		else:
			entry_date = self[0]
		return '{} {} - {}-{}'.format(entry_date, *self[1:])
	
	@property
	def entry_date(self):
		"""
		
		:return:
		"""
		
		return self[0]
	
	@classmethod
	def from_str(cls, entry_string, version_parser=SemanticVersion):
		"""
		
		:param str entry_string:
		:param callable? version_parser:
		:return:
		"""
		
		result = re_match(cls.ENTRY_FORMAT, entry_string)
		if result is None:
			raise ValueError("Couldn't parse the provided entry: {}".format(entry_string))
		result = result.groupdict()
		result['entry_date'] = Datetime.strptime(result['entry_date'], cls.DATE_FORMAT).date()
		result['version'] = version_parser(result['version'])
		result['release'] = Release.from_str(result['release'])
		return cls(**result)
	
	@property
	def release(self):
		"""
		
		:return:
		"""
		
		return self[3]
	
	@property
	def version(self):
		"""
		
		:return:
		"""
		
		return self[2]
	

class Changelog(dict):
	"""

	"""
	
	def __call__(self, packager, version, release, messages):
		"""

		:param packager:
		:param version:
		:param release:
		:param messages:
		:return:
		"""
		
		new_entry = ChangelogEntry(Date.today(), packager, self._version_parser(version), Release.from_str(release))
		if new_entry < list(self.keys())[-1]:
			raise ValueError('Not a valid new entry for the current changelog: {}'.format(new_entry))
		self[new_entry] = messages
		return self.reversed()
	
	def __init__(self, initial_values={}, version_parser=SemanticVersion):
		"""

		:param json_file:
		"""
		
		super().__init__({ChangelogEntry.from_str(key): value for key, value in reversed(initial_values.items())})
		sorted_entries = list(self.keys())
		sorted_entries.sort()
		if sorted_entries != list(self.keys()):
			raise RuntimeError('Invalid changelog')
		self._version_parser = version_parser
	
	def __str__(self):
		"""

		:return:
		"""
		
		result = ''
		for entry, messages in self.reversed().items():
			result += '* {}\n'.format(entry)
			for message in messages:
				result += '- {}\n'.format(message)
		return result
	
	def reversed(self):
		"""

		:return:
		"""
		
		return dict(reversed(self.items()))