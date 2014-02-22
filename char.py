
class Char:
	def __init__(self, char, prop):
		self.char=char

		self._cangjie=None
		self._array=None
		self._dayi=None
		self._boshiamy=None
		self._zhengma=None

		if len(prop)>=8:
			self.setIMproperty(prop)

	def setIMproperty(self, prop):
		self.cj=prop[1]
		self.ar=prop[2]
		self.dy=prop[3]
		self.bs=prop[4]
		self.zm=prop[6]

	@property
	def cj(self):
		return self._cangjie

	@cj.setter
	def cj(self, code):
		self._cangjie=code

	@property
	def ar(self):
		return self._array

	@ar.setter
	def ar(self, code):
		self._array=code

	@property
	def dy(self):
		return self._dy

	@dy.setter
	def dy(self, code):
		self._dy=code

	@property
	def bs(self):
		return self._bs

	@bs.setter
	def bs(self, code):
		self._bs=code

	@property
	def zm(self):
		return self._zm

	@zm.setter
	def zm(self, code):
		self._zm=code

if __name__=='__main__':
	c=Char('王', ['(龜)', 'kn', 'sl', '/c', 'k', 'l', 'qy', '12'])
	print('倉頡 ', c.cj)
	print('行列 ', c.ar)
	print('大易 ', c.dy)
	print('嘸蝦米 ', c.bs)
	print('鄭碼 ', c.zm)

