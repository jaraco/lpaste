#!/usr/bin/env python

import os, sys
from urllib import urlencode
from optparse import OptionParser
from getpass import getuser
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
register_openers()

import webbrowser

paste_url = 'http://a.libpa.st/'

def main():
	usage = 'usage: %prog [options] [file]'
	parser = OptionParser(usage=usage)

	parser.add_option('-t', '--format', dest='format', default='_')
	default_user = os.environ.get('QPASTEUSER') or os.environ.get('USERNAME') or getuser()
	parser.add_option('-u', '--username', dest='username',
					  default=default_user)
	parser.add_option('-l', '--longurl', dest='longurl', action="store_true", default=False)
	parser.add_option('-a', '--attach', dest='attach', action="store_true", default=False)
	parser.add_option('-b', '--browser', dest='browser', action="store_true", default=False)

	options, args = parser.parse_args()
	if args:
		filename = args[0]
		fh = open(filename, 'rb')
	else:
		print 'Using stdin...'
		fh = sys.stdin()

	data = {'nick': options.username, 'fmt': options.format, }
	if not options.longurl:
		data['makeshort'] = 'True'
	if options.attach:
		data['file'] = fh
		datagen, headers = multipart_encode(data)
	else:
		code = fh.read()
		fh.close()
		data['code'] = code
		datagen = urlencode(data)
		headers = {}

		
	req = urllib2.Request(paste_url, datagen, headers)
	res = urllib2.urlopen(req)
	url = res.geturl()
	print 'Paste URL: %s' % url
	if options.browser:
		print "Now opening browser..."
		webbrowser.open(url)


if __name__ == '__main__':
	main()
