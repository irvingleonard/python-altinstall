#!python
"""

"""

from simplifiedapp import main

try:
	import python_altinstall_packager
except ModuleNotFoundError:
	import __init__ as python_altinstall_packager

main(python_altinstall_packager)
