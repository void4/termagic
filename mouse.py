from pymouse import PyMouseEvent
#import traceback
from time import time

def capture_line():
	line = []
	state = False
	time_start = None

	class handler(PyMouseEvent):
		def click(self, x, y, button, d):
			nonlocal state, time_start
			if button == 1:
				if state and not d:
					self.exit()
				state = d
				time_start = time()
			return(x, y, button)

		def move(self, x, y):
			nonlocal line
			if state:
				line.append([x,y, time()-time_start])
			return x, y

	test = handler()
	try:
		test.run()
		test.join()
	except Exception as e:
		#traceback.print_exc()
		pass

	return line

def enhanced_line(line):
	newline = []
	for xyt in line:
		x,y,t = xyt
		if len(newline) == 0:
			d = 0
			v = 0
			a = 0
		else:
			last = newline[-1]
			d = ((last[0]-x)**2+(last[1]-y)**2)**0.5
			v = d/t
			a = v-last[4]

		newline.append([x,y,t,d,v,a])
	return newline
