import os

def path_to_purename(path):
	basename = os.path.basename(path)
	purename = basename.split(".")[0]
	return purename

PSIZE = 256
def scale(xy, scale=PSIZE):
	for i in range(len(xy)):
		xy[i] = [v*(scale-1) for v in xy[i]]

	return xy

def normalize(xy):
	xmi = min(xy, key=lambda x:x[0])[0]
	ymi = min(xy, key=lambda x:x[1])[1]
	for i in range(len(xy)):
		xy[i] = [xy[i][0]-xmi, xy[i][1]-ymi]
	xma = max(xy, key=lambda x:x[0])[0]
	yma = max(xy, key=lambda x:x[1])[1]
	for i in range(len(xy)):
		xy[i] = [xy[i][0]/xma, xy[i][1]/yma]

	return xy


from PIL import Image, ImageDraw

def draw(xy):
	scale(normalize(xy))
	img = Image.new("RGB", (PSIZE, PSIZE))
	draw = ImageDraw.Draw(img)

	last = xy[0]
	for i in range(1, len(xy)):
		x,y = xy[i]
		#print(x,y)
		#img.putpixel((int(x),int(y)), 0xffffff)
		#TODO add time color
		draw.line((last[0], last[1], x, y), 0xffffff)
		last = [x,y]

	return img
