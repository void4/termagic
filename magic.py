import os, sys
import argparse

from subprocess import check_output

from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard

from patterns import ImagePatternHandler

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

	return line

k = PyKeyboard()

def runonce():

	try:
		line = once()
	except:
		return

	handler = ImagePatternHandler()

	pattern = handler.input_to_pattern(line)

	#h2 = hfunc(img2)
	#print(h1, h2, h1-h2)
	if SAVE:
		handler.save_pattern(SAVE, pattern)
		raise RuntimeError("Pattern saved")

	closest = handler.closest_pattern(pattern)

	if not DAEMON and DRAW:
		sys.stdout.write(check_output("img2txt %s" % closest["path"], shell=True).decode("utf8"))

	text = closest["name"]

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
