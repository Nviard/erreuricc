	def remove_slide(self):
		if self._slides:
			to_remove = random.choice(self._slides)
			self._slides.remove(to_remove)
			for p in to_remove.all():
				self._pics.remove(p)









	def new(cls, numH, numV):
		slideshow = cls
		myhpics = list(hpics.keys())
		myvpics = list(vpics.keys())

		order = [([True] * min(numH, len(myhpics))), ([False] * min(numV, len(myvpics))/2)]
		random.shuffle(order)
		for boo in order:
			if boo:
				pic = random.choice(myhpics)
				myhpics.remove(pic)
				slideshow._pics.add(pic)
				slideshow._slides.add(HSlide(pic, hpics[pic]))
			else:
				pic1, pic2 = random.sample(myvpics)
				myvpics.remove(pic1)
				myvpics.remove(pic2)
				slideshow._pics.add(pic1)
				slideshow._pics.add(pic2)
				slideshow._slides.add(VSlide(pic1, vpics[pic1], pic2, vpics[pic2]))

		return slideshow