#!/usr/bin/env python

import os, sys
from urllib import urlencode
from optparse import OptionParser
import ConfigParser
import getpass
from poster.encode import multipart_encode, MultipartParam
import poster.streaminghttp
import urllib2
import webbrowser
from . import keyring


BASE_HEADERS = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2b1) lpaste'}

def install_opener(*handlers):
	opener = poster.streaminghttp.register_openers()
	map(opener.add_handler, handlers)

def main():

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

	default_user = file_user or os.environ.get('QPASTEUSER') or os.environ.get('USERNAME') or getpass.getuser()

	usage = 'usage: %prog [options] [file]'
	parser = OptionParser(usage=usage)

	parser.add_option('-s', '--site', dest='site',
		default=default_url, help="URL for the library paste site to use. By default: %s" % default_url)
	parser.add_option('-t', '--format', dest='format', default='_',
		help="Which syntax code highlighter would you like to use? Defaults to plain text.")
	parser.add_option('-u', '--username', dest='username',
		default=default_user, help="Username to paste as, attempts to use system account name if none specified.")
	parser.add_option('-l', '--longurl', dest='longurl', action="store_true", default=False,
		help="Use a long url instead of the default short")
	parser.add_option('-a', '--attach', dest='attach', action="store_true", default=False,
		help="Upload the file as an attachment instead of as code/text")
	parser.add_option('-b', '--browser', dest='browser', action="store_true", default=False,
		help="Open your paste in a new browser window after it's uploaded")
	parser.add_option('--auth-username', default=default_user,
		help="The username to use when HTTP auth is required",)
	if not keyring.enabled:
		parser.add_option('--auth-password',
			help="The password to use when HTTP auth is required",)
	options, args = parser.parse_args()
	if args and args[0] != '-':
		filename = args[0]
		fh = open(filename, 'rb')
	else:
		print 'Using stdin...'
		fh = sys.stdin

	paste_url = options.site
	data = {'nick': options.username, 'fmt': options.format, }
	if not options.longurl:
		data['makeshort'] = 'True'
	if options.attach:
		data = data.items()
		data.append(MultipartParam.from_file('file', filename))
		datagen, headers = multipart_encode(data)
		headers.update(BASE_HEADERS)
	else:
		code = fh.read()
		fh.close()
		data['code'] = code
		datagen = urlencode(data)
		headers = BASE_HEADERS

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
	res = urllib2.urlopen(req)
	url = res.geturl()
	print 'Paste URL: %s' % url
	if options.browser:
		print "Now opening browser..."
		webbrowser.open(url)


if __name__ == '__main__':
	main()
