import abc
import mimetypes
from poster.encode import MultipartParam

# add mimetypes not present in Python
mimetypes.add_type('image/svg+xml', '.svg')
mimetypes.add_type('application/json', '.json')

class Source(object):
	@abc.abstractmethod
	def apply(self, data):
		"Apply this source to the data"

class CodeSource(Source):
	def __init__(self, code):
		self.code = code

	def apply(self, data):
		data['code'] = self.code

class FileSource(Source):
	def __init__(self, stream, content_type=None, filename=None):
		self.stream = stream
		self.content_type = content_type
		self.filename = filename

	def apply(self, data):
		if self.filename and not self.content_type:
			self.content_type, _ = mimetypes.guess_type(self.filename)
		if not self.content_type:
			self.content_type = 'application/octet-stream'
		params = dict(
			fileobj = self.stream,
			filetype = self.content_type,
		)
		if self.filename: params.update(filename=self.filename)
		data['file'] = MultipartParam('file', **params)
