import time
import os
import Image

def GetAllFiles(folder):
	files = os.listdir(folder)
	output = []
	for file in files:
		path = os.path.join(folder, file)
		if os.path.isdir(path):
			output += GetAllFiles(path)
		else:
			if path.endswith('.png') or path.endswith('.jpg'):
				output.append(path)
	return output


def ConvertFile(path):
	print "Converting " + path + '...'
	
	original = Image.open(path)
	if original.mode != 'RGBA':
		original = original.convert('RGBA')
	
	pixels = original.load()
	width = original.size[0]
	height = original.size[1]
	
	x = 0
	while x < width:
		
		y = 0
		while y < height:
			
			v = pixels[x, y]
			gray = int((0.0 + v[0] + v[1] + v[2]) / 3)
			pixels[x, y] = (gray, gray, gray, v[3])
			
			y += 1
		x += 1
	
	original.save('Gray' + path)

files = GetAllFiles('Images' + os.sep + 'Tiles') + GetAllFiles('Images' + os.sep + 'Sprites')
for file in files:
	ConvertFile(file)