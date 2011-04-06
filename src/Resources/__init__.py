from . import imagelibrary as _imglib
ImageLibrary = _imglib.ImageLibrary()

from . import font as _font
GetFont = _font.GetFont

from . import ttf_font as _ttf
TTF_Font = _ttf.TTF_Font

from . import border as _border
Border = _border.Border

_borderObj = None

def CreateBorder(width, height):
	global _borderObj
	if _borderObj == None:
		_borderObj = Border()
	return _borderObj.MakeSurf(width // 16, height // 16)
