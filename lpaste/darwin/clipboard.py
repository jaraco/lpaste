import richxerox

from lpaste.source import CodeSource, FileSource

def do_html():
	snippet = richxerox.paste('html')
	return FileSource.from_snippet(snippet)

def do_text():
	code = richxerox.paste()
	src = CodeSource(code=code)
	src.check_python()
	return src

def get_source():
	try:
		do_html()
	except:
		pass

	return do_text()

set_text = richxerox.copy
