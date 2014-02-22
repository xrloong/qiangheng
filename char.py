
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
		if code=='XXXX':
			self._cangjie=None
		else:
			self._cangjie=code

	@property
	def ar(self):
		return self._array

	@ar.setter
	def ar(self, code):
		if code=='XXXX':
			self._array=None
		else:
			self._array=code

	@property
	def dy(self):
		return self._dayi

	@dy.setter
	def dy(self, code):
		if code=='XXXX':
			self._dayi=None
		else:
			self._dayi=code

	@property
	def bs(self):
		return self._boshiamy

	@bs.setter
	def bs(self, code):
		if code=='XXXX':
			self._boshiamy=None
		else:
			self._boshiamy=code

	@property
	def zm(self):
		return self._zhengma

	@zm.setter
	def zm(self, code):
		if code=='XXXX':
			self._zhengma=None
		else:
			self._zhengma=code

if __name__=='__main__':
	c=Char('王', ['(龜)', 'kn', 'sl', '/c', 'k', 'l', 'qy', '12'])
	print('倉頡 ', c.cj)
	print('行列 ', c.ar)
	print('大易 ', c.dy)
	print('嘸蝦米 ', c.bs)
	print('鄭碼 ', c.zm)

