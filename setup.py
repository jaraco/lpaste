#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import setuptools

name = 'lpaste'
description = 'Library Paste command-line client'
nspkg_technique = 'native'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
	name=name,
	use_scm_version=True,
	author="Chris Mulligan",
	author_email="chmullig@gmail.com",
	mainainer="Jason R. Coombs",
	maintainer_email="jaraco@jaraco.com",
	description=description or name,
	url="https://github.com/jaraco/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=(
		name.split('.')[:-1] if nspkg_technique == 'managed'
		else []
	),
	python_requires='>=3.5',
	install_requires=[
		'requests',
		'keyring>=0.6',
		'jaraco.context',
		'jaraco.clipboard',
	],
	extras_require={
		'testing': [
			# upstream
			'pytest>=3.5,!=3.7.3',
			'pytest-sugar>=0.9.1',
			'collective.checkdocs',
			'pytest-flake8',

			# local
		],
		'docs': [
			# upstream
			'sphinx',
			'jaraco.packaging>=3.2',
			'rst.linker>=1.9',

			# local
		],
		'clipboard': 'jaraco.clipboard',
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'console_scripts': [
			'lpaste=lpaste.lpaste:main',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
