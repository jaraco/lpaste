from __future__ import absolute_import

import getpass

try:
	import keyring
except ImportError:
	pass
enabled = 'keyring' in globals()

from keyring.http import PasswordMgr

class FixedUserKeyringPasswordManager(PasswordMgr):
	def __init__(self, username):
		self.username = username

	def get_username(self, realm, authuri):
		return self.username

