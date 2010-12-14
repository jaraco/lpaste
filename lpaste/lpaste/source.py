from poster.encode import MultipartParam

class Source(object):
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	@classmethod
	def from_stream(cls, stream,
		content_type='application/octet-stream', filename=None):
		source = Source(stream=stream)
		source.content_type = content_type
		source.filename = filename
		return source

	def apply(self, data):
		if hasattr(self, 'code'):
			data['code'] = self.code
			return
		data['file'] = MultipartParam('file',
			filetype = self.content_type,
			fileobj = self.stream,
			filename = self.filename,
			)
