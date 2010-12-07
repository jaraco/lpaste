from setuptools import setup

setup(name="lpaste",
	version="0.1",
	packages=['lpaste'],
	entry_points = {
		'console_scripts': [
			'lpaste = lpaste.lpaste:main',
		],
	},
	install_requires = [
		'poster', 
	],
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
		'Programming Language :: Python :: 2.5',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
	],
)

