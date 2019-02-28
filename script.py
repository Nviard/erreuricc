	def remove_slide(self):
		if self._slides:
			to_remove = random.choice(self._slides)
			self._slides.remove(to_remove)
			for p in to_remove.all():
				self._pics.remove(p)