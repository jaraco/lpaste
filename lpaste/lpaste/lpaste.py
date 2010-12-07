#!/usr/bin/env python
from __future__ import absolute_import

import os, sys
from urllib import urlencode
from optparse import OptionParser
import ConfigParser
from getpass import getuser
from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib2
import webbrowser

try:
	lpaste = __import__('lpaste.%s.clipboard' % sys.platform)
	clipb = getattr(lpaste, sys.platform).clipboard
except ImportError:
	raise RuntimeError("No clipboard support")
	clipb = None

register_openers()
BASE_HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2b1) lpaste'}

def get_options():
	"""
	%prog [options]
	
	By default, %prog will take the content from the clipboard. Use the
	`file` parameter to pass in a file or use stdin.
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

	parser = OptionParser(usage=get_options.__doc__)

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
	parser.add_option('-f', '--file',
		help="Paste the content from the file (use '-' for stdin); "
		"otherwise, content will be taken from the clipboard")

	options, args = parser.parse_args()
	if getattr(options, 'file', None):
		stream = open(options.file, 'rb') if options.file != '-' else sys.stdin
		if options.attach:
			source = Source.from_stream(stream)
		else:
			source = Source(code=stream.read())
	else:
		source = clipb.get_source()

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
	clipb.set_text(url)
	print 'Paste URL: %s' % url
	if options.browser:
		print "Now opening browser..."
		webbrowser.open(url)


if __name__ == '__main__':
	main()
