from glob import glob
import sys
import os

from PIL import Image
import imagehash

from util import path_to_purename, draw


class ImagePatternHandler:
	def __init__(self, PATTERNDIR="patterns"):
		self.PATTERNDIR = PATTERNDIR

		os.makedirs(self.PATTERNDIR, exist_ok=True)
		# TODO test imagehash.average_hash, imagehash.phash
		self.hashfunc = imagehash.dhash_vertical
		self.load_patterns()

	def load_patterns(self):
		patternpaths = glob(os.path.join(self.PATTERNDIR, "*.png"))

		self.patterns = []

		for patternpath in patternpaths:
			patternimage = Image.open(patternpath)
			patternhash = self.hashfunc(patternimage)
			patternname = path_to_purename(patternpath)
			self.patterns.append({"name": patternname, "image":patternimage, "hash": patternhash, "path": patternpath})

	def input_to_pattern(self, line):
		patternimage = draw(line)
		patternhash = self.hashfunc(patternimage)
		return {"name": None, "image": patternimage, "hash": patternhash, "path": None}

	def closest_pattern(self, pattern):
		if len(self.patterns) == 0:
			#raise
			return None

		closest = min(self.patterns, key=lambda p:p["hash"]-pattern["hash"])
		return closest

	def save_pattern(self, name, pattern):
		patternpath = os.path.join(self.PATTERNDIR, name+".png")
		pattern["image"].save(patternpath)
		# To include the new one. Could be more efficient, but hey
		self.load_patterns()

import traj_dist.distance as tdist
import numpy as np
import json

class PathPatternHandler:
	def __init__(self, PATTERNDIR="patterns"):
		self.PATTERNDIR = PATTERNDIR
		self.distance = tdist.frechet
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
			self.patterns.append({"name": patternname, "data":patterndata, "path": patternpath})

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
		patternpath = os.path.join(self.PATTERNDIR, name+".txt")
		with open(patternpath, "w+") as patternfile:
			patternfile.write(json.dumps(pattern["data"]))
		# To include the new one. Could be more efficient, but hey
		self.load_patterns()
