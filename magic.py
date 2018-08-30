from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard
import os, sys
import argparse
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

k = PyKeyboard()

def runonce():

	try:
		img1 = once()
	except:
		return
	#img2 = once()
	#img.show()
	import imagehash

	# TODO test imagehash.average_hash, imagehash.phash
	hfunc = imagehash.dhash_vertical

	h1 = hfunc(img1)
	#h2 = hfunc(img2)
	#print(h1, h2, h1-h2)
	if SAVE:
		img1.save("patterns/%s.png" % SAVE)
		raise RuntimeError("Pattern saved")

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

	if not DAEMON and DRAW:
		sys.stdout.write(check_output("img2txt %s" % mptn[1], shell=True).decode("utf8"))

	basename = os.path.basename(mptn[1])
	text = basename.split(".")[0]

	if text == "exit":
		raise RuntimeError("Exiting...")

	k.type_string(text+" ")
	
	if EXEC:
		k.tap_key("Return")


LOOP = False
EXEC = False
DRAW = False
SAVE = False
DAEMON = False

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Execute commands by tracing shapes with your cursor")
	parser.add_argument("--loop", dest="loop", action="store_const", const=True, default=False, help="loop indefinitely, draw an x to exit")
	parser.add_argument("--exec", dest="exec", action="store_const", const=True, default=False, help="execute commands immediately")
	parser.add_argument("--draw", dest="draw", action="store_const", const=True, default=False, help="draw the recognized shape as ascii image")
	parser.add_argument("--save", dest="save", action="store", default=False, help="save a custom shape and command")
	parser.add_argument("--daemon", dest="daemon", action="store_const", const=True, default=False, help="run this app in the background")
	args = parser.parse_args()
	
	LOOP = args.loop
	EXEC = args.exec
	DRAW = args.draw
	SAVE = args.save
	DAEMON = args.daemon
			
	if DAEMON:
		fpid = os.fork()
		#print(fpid)
		if fpid != 0:
			sys.exit(0)
		
	while True:
		try:
			runonce()
		except RuntimeError as e:
			print(str(e))
			break
		if not LOOP or SAVE:
			break
