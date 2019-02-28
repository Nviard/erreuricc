import numpy as np

class Slideshow():
	def __init__(self):
		self._slides = []

	def score(self):
		res = 0
		for n in range(len(self._slides) - 1):
			s = self._slides[n]
			t = self._slides[n+1]
			res += min(len(s & t), len(s - t), len(t-s))
		return res

class VSlide(Slide):
	def __init__(self, O1, tags1, O2, tags2):
		self._O1 = O1
		self._O2 = O2
		self._tags = set([*tags1, *tags2])

class HSlide(Slide):
	def __init__(self, tags):
		self._tags = set(tags)

N = int(input())

vpics = {}
hpics = {}

for i in range(N):
	O, M, *tags = input().split()
	if M == "V":
		vslides[O]=(set(tags))
	else:
		hslides[O]=(set(tags))
