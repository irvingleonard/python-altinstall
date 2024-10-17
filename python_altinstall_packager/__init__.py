#!python
"""

"""

from atexit import register as atexit_register
from json import dumps as json_dumps, loads as json_loads
from logging import getLogger
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from urllib.parse import urlparse

from requests import get as requests_get

try:
	from jinja2 import Environment as Jinja2Environment
except ImportError:
	Jinja2Environment = None
try:
	from docker import from_env as docker_from_env
except ImportError:
	docker_from_env = None

from . import _data as DATA
from .specfile_ import Changelog

__version__ = '0.1.0.dev0'

LOGGER = getLogger(__name__)


class SpecfileTemplate(dict):
	"""
	
	"""
	
	TEMPLATE_NAME = 'specfile.jinja'
	_values_loaded = False
	
	def __call__(self, destination_dir=Path.cwd()):
		"""
		
		:param destination_dir:
		:return:
		"""
		
		pass
	
	def __getattr__(self, item):
		"""

		"""
		
		if item == 'distro_data':
			if self.dist not in DATA.distributions:
				raise ValueError('Missing "{}" distribution in knowledge base'.format(self.dist))
			value = DATA.distributions[self.dist]
		elif item == 'python_data':
			for ver_len in range(len(self['python_version']), -1, -1):
				python_version = '.'.join(self['python_version'][:ver_len])
				if not python_version:
					raise ValueError('Missing "{}" python in knowledge base'.format(python_version))
				if python_version in DATA.python:
					value = DATA.python[python_version]
					break
		elif item == 'template_file_path':
			value = Path(__file__).parent / 'data' / self.TEMPLATE_NAME
			if not value.is_file():
				raise FileNotFoundError('Specfile template not found "{}"'.format(value))
		else:
			raise AttributeError(item)
		
		self.__setattr__(item, value)
		return value
	
	def __init__(self, dist, python_version, changelog_file='changelog.json', /, **details):
		"""
		
		"""
		
		super().__init__(details)
		self.dist = dist
		if isinstance(python_version, str):
			python_version = python_version.split('.')
		self['python_version'] = python_version
		self['package_name'] = 'python{}-altinstall'.format(''.join(python_version[:2]))
		self.changelog_file = Path(changelog_file)
	
	def __str__(self):
		"""

		"""
		
		if Jinja2Environment is None:
			raise ImportError('The "jinja2" package is required by {}'.format(type(self).__name__))
		jinja_env = Jinja2Environment()
		result = jinja_env.from_string(self.template_file_path.read_text())
		self._load_values()
		return result.render(self)
	
	def _load_values(self):
		"""
		
		:return:
		"""
		
		if 'build_number' not in self:
			self['build_number'] = 1
		if 'requires' in self.distro_data:
			self['requires'] = self.distro_data['requires']
		self.update(self.python_data)
		self['changelog'] = Changelog(json_loads(self.changelog_file.read_text()))
		
	def write_file(self, specs_dir=Path.cwd()):
		"""
		
		:param specs_dir:
		:return:
		"""
		
		specs_dir = Path(specs_dir)
		specs_dir.mkdir(parents=True, exist_ok=True)
		file_name = specs_dir / (self['package_name'] + '.spec')
		file_name.write_text(str(self))
		return file_name


class DockerfileTemplate(dict):
	"""

	"""
	
	TAG_NAME = 'python_altinstall_packager'
	TEMPLATE_NAMES = 'dockerfile_{}_template.jinja'
	
	def __enter__(self):
		"""

		"""
		
		self.dockerfile.write_text(str(self))
		return self.dockerfile
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		"""

		"""
		
		LOGGER.debug('Ignoring exception in context: %s(%s) | %s', exc_type, exc_val, exc_tb)
		if not self._keep_file:
			self.dockerfile.unlink(missing_ok=True)
	
	def __getattr__(self, item):
		"""

		"""
		
		if item == 'client':
			if docker_from_env is None:
				raise ImportError('The "docker" package is required by {}'.format(type(self).__name__))
			value = docker_from_env()
		elif item == 'defaults':
			if self.dist not in DATA.distributions:
				raise ValueError('Missing "{}" distribution in knowledge base'.format(self.dist))
			value = DATA.distributions[self.dist]
			if 'dockerfile' in value:
				self.update(value['dockerfile'])
		elif item == 'dockerfile':
			value = self.root_dir / 'Dockerfile'
		elif item == 'packaging_tool':
			if 'packaging_tool' not in self.defaults:
				raise ValueError('Missing "packaging_tool" section for "{}" distribution in knowledge base'.format(self.dist))
			value = self.defaults['packaging_tool']
		elif item == 'template_file_path':
			value = Path(__file__).parent / 'data' / self.TEMPLATE_NAMES.format(self.packaging_tool)
			if not value.is_file():
				raise FileNotFoundError('Dockerfile template not found for "{}"'.format(self.packaging_tool))
		else:
			raise AttributeError(item)
		
		self.__setattr__(item, value)
		return value
	
	def __init__(self, dist, python_version, root_dir=Path.cwd(), keep_file=False, /, **details):
		"""

		"""
		
		super().__init__(details)
		self.root_dir = Path(root_dir)
		self.dist = dist
		if isinstance(python_version, str):
			python_version = python_version.split('.')
		self.python_version = python_version
		self._keep_file = keep_file
	
	def __str__(self):
		"""

		"""
		
		if Jinja2Environment is None:
			raise ImportError('The "jinja2" package is required by {}'.format(type(self).__name__))
		jinja_env = Jinja2Environment()
		result = jinja_env.from_string(self.template_file_path.read_text())
		return result.render(self)
	
	def build(self, name_tag):
		"""

		"""
		
		with self as dockerfile:
			result = self.client.images.build(path=str(dockerfile.parent), tag=name_tag, rm=True, forcerm=True)
		return result
	
	def run(self, fresh_build=True, /, **run_arguments):
		"""

		"""
		
		if fresh_build:
			self.build(self.TAG_NAME)
		
		run_arguments_ = {
			'name': self.TAG_NAME + '_temp',
			'remove': True,
			'stderr': True,
			'stdout': True,
		}
		run_arguments_.update(run_arguments)
		return self.client.containers.run(self.TAG_NAME, **run_arguments_)
	
	def write_file(self, output_dir=None):
		"""
		
		:return:
		"""
		
		if output_dir is None:
			dockerfile = self.dockerfile
		else:
			dockerfile = Path(output_dir) / 'Dockerfile'
		return dockerfile.write_text(str(self))


class PythonAltinstallPackager:
	"""
	
	"""
	
	DOWNLOAD_PATH_TEMPLATE = r'https://www.python.org/ftp/python/{version}/Python-{version}.tgz'
	
	def __init__(self, dist_dir=Path.cwd()):
		"""
		
		:param build_dir:
		"""
		
		self._dist_dir = dist_dir
		# if build_dir is None:
		# 	self._build_dir = Path(mkdtemp()).absolute()
		# 	atexit_register(rmtree, build_dir, ignore_errors=True)
		# else:
		# 	self._build_dir = Path(build_dir)
	
	def build(self, *versions, distributions=None):
		"""
		
		:param versions:
		:param distributions:
		:return:
		"""
		
		if distributions is None:
			distributions = tuple(DATA.distributions.keys())
		
		for version in versions:
			print(version, distributions)
	
	def download_tarball(self, version, stream_chunk_size=1048576, destination_dir=None, overwrite=False):
		"""
		
		:param version:
		:param stream_chunk_size:
		:param destination_dir:
		:param overwrite:
		:return:
		"""
		
		download_url = self.DOWNLOAD_PATH_TEMPLATE.format(version=version)
		destination_dir = Path.cwd() if destination_dir is None else Path(destination_dir)
		destination_dir.mkdir(exist_ok=True)
		local_file = destination_dir / Path(urlparse(download_url).path).name
		if local_file.exists() and not overwrite:
			return local_file
		else:
			local_file.unlink(missing_ok=True)
		
		with requests_get(download_url, stream=True) as source_file:
			source_file.raise_for_status()
			with open(local_file, 'wb') as file_obj:
				for chunk in source_file.iter_content(chunk_size=stream_chunk_size):
					file_obj.write(chunk)
		
		return local_file
	
	def prepare_build(self, dist, python_version, output_directory=None):
		"""
		
		:return:
		"""
		
		if output_directory is None:
			output_directory = self._build_dir
		else:
			output_directory = Path(output_directory)
		output_directory.mkdir(parents=True, exist_ok=True)
		self.download_tarball(version=python_version, destination_dir=(output_directory / 'SOURCES'))
		SpecfileTemplate(dist, python_version).write_file(specs_dir=(output_directory / 'SPECS'))
		DockerfileTemplate(dist, python_version).write_file(output_dir=output_directory)
	
	def test(self):
		
		from .specfile_ import Changelog, ChangelogEntry
		
		# value = ChangelogEntry.from_str('Thu Oct 3 2024 Irving Leonard <irvingleonard@github.com> 3.12.7-1')
		# return value
		# return str(value)
		#
		# value = ChangelogEntry(date.today(), 'Irv LEo <irvleo@example.net>', '4.5.6-10')
		# return str(value)
		# changelog_file = Path('changelog.json')
		# ch = Changelog(json_loads(changelog_file.read_text()))
		# return ch
		# return str(ch)
		# return ch('Irv LEo <irvleo@example.net>', '4.5.6', '11', ['new testing'])
		
		# return str(SpecfileTemplate('el9', '3.10.20'))
		
		test_dir = Path.cwd() / 'testing'
		
		test_dir.mkdir(exist_ok=True)
		with DockerfileTemplate('el9', '3.10.20', test_dir, True) as dockerfile:
			pass
		