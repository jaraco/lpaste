import pyperclip

from lpaste.source import CodeSource

def get_source():
	code = pyperclip.paste()
	src = CodeSource(code=code)
	src.check_python()
	return src

set_text = pyperclip.copy
