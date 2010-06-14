from setuptools import setup

setup(name="qpaste",
	version="0.0.1",
	packages=['qpaste'],
	entry_points = {
		'console_scripts': [
			'qpaste = qpaste.qpaste:main',
		],
	},
	install_requires = [
		'poster', 
	],
)

