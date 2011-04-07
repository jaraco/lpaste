from __future__ import absolute_import

try:
	import keyring
except ImportError:
	pass
enabled = 'keyring' in globals()

try:
	from keyring.http import PasswordMgr
except ImportError:
	# keep a copy until keyring 0.6
	class PasswordMgr(object):
		def get_username(self, realm, authuri):
			return getpass.getuser()

		def find_user_password(self, realm, authuri):
			user = self.get_username(realm, authuri)
			passwd = keyring.get_password(authuri, user)
			if passwd is None:
				prompt = 'password for %(user)s@%(realm)s for '\
					'%(authuri)s: ' % vars()
				passwd = getpass.getpass(prompt)
				keyring.set_password(authuri, user, passwd)
			return user, passwd

class FixedUserKeyringPasswordManager(PasswordMgr):
	def __init__(self, username):
		self.username = username

	def get_username(self, realm, authuri):
		return self.username

