#!/usr/bin/env python
from __future__ import absolute_import

import os
import sys
from optparse import OptionParser
import ConfigParser
import getpass
from poster.encode import multipart_encode
import poster.streaminghttp
import urllib2
import webbrowser
from textwrap import dedent
from . import keyring

try:
	lpaste = __import__('lpaste.%s.clipboard' % sys.platform)
	clipb = getattr(lpaste, sys.platform).clipboard
except ImportError:
	clipb = None
from lpaste.source import Source

BASE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2b1) lpaste'}

def install_opener(*handlers):
	opener = poster.streaminghttp.register_openers()
	map(opener.add_handler, handlers)

def get_options():
	"""
	%prog [options] [<file>]

	If file is not suplied, stdin will be used.
	"""
	fileconf = ConfigParser.ConfigParser()
	fileconf.read('/etc/lpasterc')
	fileconf.read(os.path.expanduser('~/.lpasterc'))
	try:
		default_url = fileconf.get('lpaste', 'url')
	except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
		default_url = 'http://a.libpa.st/'
	try:
		file_user = fileconf.get('lpaste', 'user')
	except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
		file_user = ''

	default_user = (file_user or os.environ.get('QPASTEUSER')
		or os.environ.get('USERNAME') or getuser())

	parser = OptionParser(usage=dedent(get_options.__doc__).lstrip())

	parser.add_option('-s', '--site', dest='site',
		default=default_url,
		help="URL for the library paste site to use. By default: %s" %
		default_url)
	parser.add_option('-t', '--format', dest='format', default='_',
		help="Which syntax code highlighter would you like to use? "
		"Defaults to plain text.")
	parser.add_option('-u', '--username', dest='username',
		default=default_user, help="Username to paste as, attempts to "
		"use system account name if none specified.")
	parser.add_option('-l', '--longurl', dest='longurl',
		action="store_true", default=False,
		help="Use a long url instead of the default short")
	parser.add_option('-a', '--attach', dest='attach',
		action="store_true", default=False,
		help="Upload the file as an attachment instead of as code/text")
	parser.add_option('-b', '--browser', dest='browser',
		action="store_true", default=False,
		help="Open your paste in a new browser window after it's "
		"uploaded")
	parser.add_option('-c', '--clipboard',
		action="store_true", default=False,
		help="Get the input from the clipboard")
	parser.add_option('--auth-username', default=default_user,
		help="The username to use when HTTP auth is required",)
	if not keyring.enabled:
		parser.add_option('--auth-password',
			help="The password to use when HTTP auth is required",)
	options, args = parser.parse_args()
	options.file = args.pop() if args else None
	if args:
		parser.error("At most one positional arg (file) is allowed.")
	if options.file and options.clipboard:
		parser.error("Either supply a file or --clipboard, but not both")
	if options.clipboard:
		if not clipb:
			parser.error("Clipboard support not available - you must "
				"supply a file")
		source = clipb.get_source()
	else:
		use_stdin = options.file in (None, '-')
		stream = open(options.file, 'rb') if not use_stdin else sys.stdin
		filename = os.path.basename(options.file) if not use_stdin else None
		if options.attach:
			source = Source.from_stream(stream, filename=filename)
		else:
			source = Source(code=stream.read())

	options.source = source
	if hasattr(source, 'format'):
		options.format = source.format
	return options


def main():

	options = get_options()

	paste_url = options.site
	data = {'nick': options.username, 'fmt': options.format, }
	if not options.longurl:
		data['makeshort'] = 'True'
	options.source.apply(data)
	datagen, headers = multipart_encode(data)
	headers.update(BASE_HEADERS)

	if keyring.enabled:
		auth_manager = keyring.FixedUserKeyringPasswordManager(options.auth_username)
	else:
		auth_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
		auth_manager.add_password(None, options.site,
			options.auth_username,
			options.auth_password or getpass.getpass())
	auth_handler = urllib2.HTTPBasicAuthHandler(auth_manager)
	install_opener(auth_handler)
	req = urllib2.Request(paste_url, datagen, headers)
	try:
		res = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		if e.getcode() != 500:
			raise
		import pdb; pdb.set_trace()
	url = res.geturl()
	if clipb: clipb.set_text(url)
	print 'Paste URL: %s' % url
	if options.browser:
		print "Now opening browser..."
		webbrowser.open(url)


if __name__ == '__main__':
	main()
