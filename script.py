import numpy as np
import random
import sys
import copy

random.seed(0)

iterations = 1000
gen_size = 2000

proba_switch_vorder = 0.15
proba_switch_horder = 0.15
proba_switch_vh = 0.15

proba_new_vorder = 0.10
proba_new_horder = 0.10
proba_new_vh = 0.10

proba_mut_vorder = 0.8
proba_mut_horder = 0.8
proba_mut_vh = 0.8

vpics = []
hpics = []
vindices = []
hindices = []

class Slideshow():

	def __init__(self, vorder, horder, vh):
		self._vorder = vorder
		self._horder = horder
		self._vh = vh

	@classmethod
	def new(cls):
		vorder = list(range(len(vpics)))
		horder = list(range(len(hpics)))
		vh = [*([True]*(len(vpics)//2)), *([False]*len(hpics))]
		random.shuffle(vorder)
		random.shuffle(horder)
		random.shuffle(vh)
		res = cls(vorder, horder, vh)

		return res

	@classmethod
	def copy(cls, other):
		res = cls(other._vorder.copy(), other._horder.copy(), other._vh.copy())
		return res

	def score(self):
		res = 0
		i_v = 0
		i_h = 0
		previous_set = set([])
		for boo in self._vh:
			if boo:
				current_set = vpics[self._vorder[i_v]] | vpics[self._vorder[i_v+1]]
				i_v += 2
			else:
				current_set = hpics[self._horder[i_h]]
				i_h += 1
			res += min(len(current_set & previous_set), len(current_set - previous_set), len(previous_set-current_set))
			previous_set = current_set

		return res

	def __repr__(self):
		res = "%d\n" % len(self._vh)
		i_v = 0
		i_h = 0
		for boo in self._vh:
			if boo:
				res += "%d %d\n" % (vindices[self._vorder[i_v]], vindices[self._vorder[i_v+1]])
				i_v += 2
			else:
				res += "%d\n" % hindices[self._horder[i_h]]
				i_h += 1

		return res


class Generation():
	def __init__(self, size):
		self._slideshows = [Slideshow.new() for s in range(size)]


	def mutation(self):
		
		random.shuffle(self._slideshows)
		res = []

		for s in self._slideshows:

			r = random.random()
			if random.random() < proba_mut_vorder:
				current = Slideshow.copy(s)
				a, b = random.sample(range(len(current._vorder)), 2)
				current._vorder[b], current._vorder[a] = current._vorder[a], current._vorder[b]
				res.append(current)

			r = random.random()
			if random.random() < proba_mut_horder:
				current = Slideshow.copy(s)
				a, b = random.sample(range(len(current._horder)), 2)
				current._horder[b], current._horder[a] = current._horder[a], current._horder[b]
				res.append(current)

			r = random.random()
			if random.random() < proba_mut_vh:
				current = Slideshow.copy(s)
				a, b = random.sample(range(len(current._vh)), 2)
				current._vh[b], current._vh[a] = current._vh[a], current._vh[b]
				res.append(current)

			r = random.random()
			if random.random() < proba_new_vorder:
				current = Slideshow.copy(s)
				random.shuffle(current._vorder)
				res.append(current)

			r = random.random()
			if random.random() < proba_new_horder:
				current = Slideshow.copy(s)
				random.shuffle(current._horder)
				res.append(current)

			r = random.random()
			if random.random() < proba_new_vh:
				current = Slideshow.copy(s)
				random.shuffle(current._vh)
				res.append(current)
		for i in range(len(self._slideshows) // 2):

			r = random.random()
			if random.random() < proba_switch_vorder:
				c1, c2 = Slideshow.copy(self._slideshows[i*2]), Slideshow.copy(self._slideshows[i*2+1])
				c1._vorder, c2._vorder = c2._vorder, c1._vorder
				res.append(c1)
				res.append(c2)

			r = random.random()
			if random.random() < proba_switch_horder:
				c1, c2 = Slideshow.copy(self._slideshows[i*2]), Slideshow.copy(self._slideshows[i*2+1])
				c1._horder, c2._horder = c2._horder, c1._horder
				res.append(c1)
				res.append(c2)

			r = random.random()
			if random.random() < proba_switch_vh:
				c1, c2 = Slideshow.copy(self._slideshows[i*2]), Slideshow.copy(self._slideshows[i*2+1])
				c1._vh, c2._vh = c2._vh, c1._vh
				res.append(c1)
				res.append(c2)

		self._slideshows.extend(res)

	def selection(self):
		random.shuffle(self._slideshows)
		start = max(0, 2 * gen_size - len(self._slideshows))
		new_slideshows = self._slideshows[:start]
		for i in range(start, gen_size, 2):
			c1 = self._slideshows[i]
			c2 = self._slideshows[i+1]
			if c1.score() > c2.score():
				new_slideshows.append(c1)
			else:
				new_slideshows.append(c2)
		
		best = self.best()
		if best not in new_slideshows:
			new_slideshows.append(best)

		self._slideshows = new_slideshows

		return self

	def best(self):
		best_score = -1
		for s in self._slideshows:
			score = s.score()
			if score > best_score:
				best_score = score
				best_slideshow = s
		print("score " + str(best_score), file=sys.stderr)
		return best_slideshow

N = int(input())

for i in range(N):
	O, M, *tags = input().split()
	if O == "V":
		vpics.append(set(tags))
		vindices.append(i)
	else:
		hpics.append(set(tags))
		hindices.append(i)

if len(vpics) == 0:
	proba_switch_vorder = 0.
	proba_switch_horder = 0.
	proba_switch_vh = 0.

	proba_new_vorder = 0.
	proba_new_vh = 0.

	proba_mut_vorder = 0.
	proba_mut_vh = 0.

if len(hpics) == 0:
	proba_switch_vorder = 0.
	proba_switch_horder = 0.
	proba_switch_vh = 0.

	proba_new_horder = 0.
	proba_new_vh = 0.

	proba_mut_horder = 0.
	proba_mut_vh = 0.


generation = Generation(gen_size)
for it in range(iterations):
	print("iteration %d" % it, file=sys.stderr)
	generation.mutation()
	generation.selection()


print(generation.best())
