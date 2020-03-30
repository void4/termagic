from glob import glob
import json
import sys
import os

import numpy as np
import traj_dist.distance as tdist

from util import path_to_purename, draw

class PathPatternHandler:
	def __init__(self, PATTERNDIR="patterns"):
		self.PATTERNDIR = PATTERNDIR
		self.distance = tdist.dtw
		os.makedirs(self.PATTERNDIR, exist_ok=True)
		# TODO test imagehash.average_hash, imagehash.phash
		self.load_patterns()

	def load_patterns(self):
		patternpaths = glob(os.path.join(self.PATTERNDIR, "*.txt"))

		self.patterns = []

		for patternpath in patternpaths:
			with open(patternpath) as patternfile:
				patterndata = json.loads(patternfile.read())
			patternname = path_to_purename(patternpath)
			imagepath = patternpath.rsplit(".")[-2] + ".png"
			self.patterns.append({"name": patternname, "data":patterndata, "path": patternpath, "imagepath": imagepath})

	def input_to_pattern(self, line):
		patterndata = line
		return {"name": None, "data": patterndata, "path": None}

	def closest_pattern(self, pattern):
		if len(self.patterns) == 0:
			#raise
			return None

		closest = min(self.patterns,
			key=lambda p:self.distance(
				np.array(p["data"])[:,:2].astype("float64"),
				np.array(pattern["data"])[:,:2].astype("float64")
			)
		)
		return closest

	def save_pattern(self, name, pattern):
		patterndatapath = os.path.join(self.PATTERNDIR, name+".txt")

		with open(patterndatapath, "w+") as patternfile:
			patternfile.write(json.dumps(pattern["data"]))

		patternimagepath = os.path.join(self.PATTERNDIR, name+".png")
		img = draw(pattern["data"])
		img.save(patternimagepath)
		# To include the new one. Could be more efficient, but hey
		self.load_patterns()
