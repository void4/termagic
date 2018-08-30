from pymouse import PyMouseEvent

from util import draw

def once():
	line = []
	state = False

	class handler(PyMouseEvent):
		def click(self, x, y, button, d):
			nonlocal state
			if button == 1:
				if state and not d:
					self.exit()
				state = d
			return(x, y, button)

		def move(self, x, y):
			nonlocal line
			if state:
				line.append([x,y])
			return x, y

	test = handler()
	try:
		test.run()
		test.join()
	except:
		pass

	img = draw(line)
	return img

img1 = once()
#img2 = once()
#img.show()
import imagehash

hfunc = imagehash.dhash_vertical#imagehash.average_hash#imagehash.phash

h1 = hfunc(img1)
#h2 = hfunc(img2)
#print(h1, h2, h1-h2)
#img.save("patterns/line.png")

from glob import glob
from PIL import Image
import sys
from subprocess import check_output

patterns = glob("patterns/*.png")

ptn = []
for patternpath in patterns:
	pattern = Image.open(patternpath)
	patternhash = hfunc(pattern)
	ptn.append([h1-patternhash, patternpath])

mptn = min(ptn, key=lambda x:x[0])

sys.stdout.write(check_output("img2txt %s" % mptn[1], shell=True).decode("utf8"))

import os

basename = os.path.basename(mptn[1])
text = basename.split(".")[0]

from pykeyboard import PyKeyboard

k = PyKeyboard()

k.type_string(text+" ")
