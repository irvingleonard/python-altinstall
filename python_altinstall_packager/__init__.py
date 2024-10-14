#!python
"""

"""

from logging import getLogger
from pathlib import Path

from . import _data as DATA

try:
	from jinja2 import Environment as Jinja2Environment
except ImportError:
	Jinja2Environment = None
try:
	from docker import from_env as docker_from_env
except ImportError:
	docker_from_env = None

__version__ = '0.1.0.dev0'

LOGGER = getLogger(__name__)


class SpecfileTemplate(dict):
	"""
	
	"""
	
	KNOWLEDGE_BASE_FILE = Path(__file__).parent / 'data' / 'distros.json'
	TEMPLATE_NAME = 'specfile.jinja'
	
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
		elif item == 'packaging_tool':
			if 'packaging_tool' not in self.defaults:
				raise ValueError(
					'Missing "packaging_tool" section for "{}" distribution in knowledge base'.format(self.dist))
			value = self.defaults['packaging_tool']
		elif item == 'template_file_path':
			value = Path(__file__).parent / 'data' / self.TEMPLATE_NAME
			if not value.is_file():
				raise FileNotFoundError('Specfile template not found "{}"'.format(value))
		else:
			raise AttributeError(item)
		
		self.__setattr__(item, value)
		return value
	
	def __init__(self, dist, python_version, /, **details):
		"""
		
		"""
		
		super().__init__(details)
		if isinstance(python_version, str):
			python_version = python_version.split('.')
		self['python_version'] = python_version
	
	def __str__(self):
		"""

		"""
		
		if Jinja2Environment is None:
			raise ImportError('The "jinja2" package is required by {}'.format(type(self).__name__))
		jinja_env = Jinja2Environment()
		result = jinja_env.from_string(self.template_file_path.read_text())
		return result.render(self)


class DockerfileTemplate(dict):
	"""

	"""
	
	KNOWLEDGE_BASE_FILE = Path(__file__).parent / 'data' / 'distros.json'
	TAG_NAME = 'python_altinstall_packager'
	TEMPLATE_NAMES = 'dockerfile_{}_template.jinja'
	
	def __enter__(self):
		"""

		"""
		
		self.dockerfile = self.root_dir / 'Dockerfile'
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
	

class PythonAltinstallPackager:
	"""
	
	"""
	
	def test(self):
		
		
		# return str(SpecfileTemplate('el9', '3.10.20'))
		
		test_dir = Path.cwd() / 'testing'
		test_dir.mkdir(exist_ok=True)
		with DockerfileTemplate('el9', '3.10.20', test_dir, True) as dockerfile:
			pass
		