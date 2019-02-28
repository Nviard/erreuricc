import numpy as np
import random
import sys

random.seed(0)

iterations = 1000
gen_size = 20
proba_h = 0.7
proba_mutation = 1.0

vpics = {}
hpics = {}

class Slideshow():
	def __init__(self):
		self._slides = []
		self._pics = set([])

	def score(self):
		res = 0
		for n in range(len(self._slides) - 1):
			s = self._slides[n]._tags
			t = self._slides[n+1]._tags
			res += min(len(s & t), len(s - t), len(t-s))
		return res

	def add_slide(self):
		if random.random() < proba_h:
			available_pics = hpics.keys() - self._pics
			if len(available_pics) > 0:
				pic = random.sample(available_pics, 1)[0]
				self._slides.append(HSlide(pic, hpics[pic]))
				self._pics.add(pic)
		else:
			available_pics = vpics.keys() - self._pics
			if len(available_pics) > 1:
				pic1, pic2 = random.sample(available_pics, 2)
				self._slides.append(VSlide(pic1, vpics[pic1], pic2, vpics[pic2]))
				self._pics.add(pic1)
				self._pics.add(pic2)

		return self

	def __repr__(self):
		res = str(len(self._slides)) + "\n"
		for s in self._slides:
			res += str(s) + "\n"

		return res

class VSlide():
	def __init__(self, O1, tags1, O2, tags2):
		self._O1 = O1
		self._O2 = O2
		self._tags = set([*tags1, *tags2])

	def __repr__(self):
			return str(self._O1) + " " + str(self._O2)

class HSlide():
	def __init__(self, O, tags):
		self._O = O
		self._tags = set(tags)

	def __repr__(self):
		return str(self._O)

class Generation():
	def __init__(self):
		self._slideshows = []


	@classmethod
	def from_slides(cls, slides):
		res = cls()
		res._slides = slides
		for slide in res._slides:
			res._pics.update(slide.pics)



	def mutation(self):
		for s in self._slideshows:
			if random.random() < proba_mutation:
				self._slideshows.append(s.add_slide())
		return self

	def selection(self):
		candidates = self._slideshows.copy()
		new_slideshows = []
		while len(new_slideshows) < gen_size:
			print(len(candidates))
			c1, c2 = random.sample(candidates, 2)
			if c1.score() > c2.score():
				new_slideshows.append(c1)
				candidates.remove(c1)
			else:
				new_slideshows.append(c2)
				candidates.remove(c2)
		self._slideshows = new_slideshows
		return self

	def best(self):
		best_score = 0
		for s in self._slideshows:
			score = s.score()
			if score >= best_score:
				best_score = score
				best_slideshow = s
		print("score " + str(score), file=sys.stderr)
		return best_slideshow

N = int(input())

for i in range(N):
	O, M, *tags = input().split()
	if O == "V":
		vpics[i]=(set(tags))
	else:
		hpics[i]=(set(tags))

print("lol"	, file=sys.stderr)
generation = Generation.new(gen_size)
print("taille apres gen %d" % len(generation._slideshows), file=sys.stderr)
for it in range(iterations):
	generation.mutation()
	print("taille apres mut %d" % len(generation._slideshows), file=sys.stderr)
	generation.selection()
	print("taille apres gen %d" %len(generation._slideshows), file=sys.stderr)


print(generation.best())
