#!/usr/bin/env python
from __future__ import absolute_import

import os, sys
from urllib import urlencode
from optparse import OptionParser
import ConfigParser
from getpass import getuser
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import webbrowser
from textwrap import dedent

try:
	lpaste = __import__('lpaste.%s.clipboard' % sys.platform)
	clipb = getattr(lpaste, sys.platform).clipboard
except ImportError:
	clipb = None
from lpaste.source import Source

register_openers()
BASE_HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2b1) lpaste'}

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

	req = urllib2.Request(paste_url, datagen, headers)
	res = urllib2.urlopen(req)
	url = res.geturl()
	if clipb: clipb.set_text(url)
	print 'Paste URL: %s' % url
	if options.browser:
		print "Now opening browser..."
		webbrowser.open(url)


if __name__ == '__main__':
	main()
