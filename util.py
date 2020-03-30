import os

def path_to_purename(path):
	basename = os.path.basename(path)
	purename = basename.split(".")[0]
	return purename

PSIZE = 256
def scale(xy, scale=PSIZE):
	for i in range(len(xy)):
		xy[i] = [xy[i][0]*(scale-1), xy[i][1]*(scale-1), xy[i][2]]

	return xy

def normalize(xy):
	xmi = min(xy, key=lambda x:x[0])[0]
	ymi = min(xy, key=lambda x:x[1])[1]
	tmi = min(xy, key=lambda x:x[2])[2]
	for i in range(len(xy)):
		xy[i] = [xy[i][0]-xmi, xy[i][1]-ymi, xy[i][2]-tmi]
	xma = max(xy, key=lambda x:x[0])[0]
	yma = max(xy, key=lambda x:x[1])[1]
	tma = max(xy, key=lambda x:x[2])[2]
	for i in range(len(xy)):
		xy[i] = [xy[i][0]/xma, xy[i][1]/yma, xy[i][2]/tma]

	return xy


from PIL import Image, ImageDraw

def draw(xyt):
	scale(normalize(xyt))
	img = Image.new("RGB", (PSIZE, PSIZE))
	draw = ImageDraw.Draw(img)

	last = xyt[0]
	for i in range(1, len(xyt)):
		x,y,t = xyt[i]
		#print(x,y)
		#img.putpixel((int(x),int(y)), 0xffffff)
		#TODO add time color
		draw.line((last[0], last[1], x, y), (int(t*255),255,255))
		last = [x,y]

	return img
