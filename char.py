
class Char:
	def __init__(self, char, prop):
		self.char=char

		self._cangjie=None
		self._array=None
		self._dayi=None
		self._boshiamy=None
		self._boshiamy_supplement=None
		self._zhengma=None
		self._zhengma_type=None

		if len(prop)>=8:
			self.setIMproperty(prop)

	def setIMproperty(self, prop):
		self.cj=prop[1]
		self.ar=prop[2]
		self.dy=prop[3]
		self.bs=[prop[4], prop[5]]
		self.zm=[prop[6], prop[7]]

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
		if self._boshiamy==None or self._boshiamy_supplement==None:
			return None
		if len(self._boshiamy)<3:
			return self._boshiamy+self._boshiamy_supplement
		else:
			return self._boshiamy

	@bs.setter
	def bs(self, code):
		if code[0]=='XXXX' or code[1]=='XXXX':
			self._boshiamy=None
			self._boshiamy_supplement=None
		else:
			self._boshiamy=code[0]
			self._boshiamy_supplement=code[1]

	@property
	def zm(self):
		if self._zhengma==None or self._zhengma_type==None:
			return None
		return self._zhengma

	@zm.setter
	def zm(self, code):
		if code[0]=='XXXX' or code[1]=='XXXX':
			self._zhengma=None
			self._zhengma_type=None
		else:
			self._zhengma=code[0]
			self._zhengma_type=code[1]

if __name__=='__main__':
	c=Char('王', ['(龜)', 'kn', 'sl', '/c', 'k', 'l', 'qy', '12'])
	print('倉頡 ', c.cj)
	print('行列 ', c.ar)
	print('大易 ', c.dy)
	print('嘸蝦米 ', c.bs)
	print('鄭碼 ', c.zm)

