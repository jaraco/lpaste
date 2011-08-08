import platform
from collections import defaultdict

from setuptools import find_packages, setup

try:
	from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
	from distutils.command.build_py import build_py

# add any platform-specific requirements
clipboard_support = defaultdict(lambda: [], {
	'Windows': ['jaraco.windows>=2.1dev'],
	})[platform.system()]

setup(
	name="lpaste",
	use_hg_version=True,
	packages=find_packages(),
	entry_points = {
		'console_scripts': [
			'lpaste = lpaste.lpaste:main',
		],
	},
	install_requires = [
		'poster',
		'keyring>=0.6',
	],
	extras_require = dict(
		clipboard = clipboard_support,
	),
	description="Library Paste command-line client",
	license = 'MIT',
	author="Chris Mulligan",
	author_email="chmullig@gmail.com",
	maintainer = 'Chris Mulligan',
	maintainer_email = 'chmullig@gmail.com',
	url = 'http://bitbucket.org/chmullig/librarypaste-tools/lpaste',
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	setup_requires = [
		'hgtools',
	],
	cmdclass=dict(build_py=build_py),
)

