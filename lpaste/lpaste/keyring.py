from __future__ import absolute_import

import keyring.http

enabled = 'keyring' in globals()

base = keyring.http.PasswordMgr if enabled else object

class FixedUserKeyringPasswordManager(base):
	def __init__(self, username):
		self.username = username

	def get_username(self, realm, authuri):
		return self.username
