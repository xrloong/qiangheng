
class Char:
	def __init__(self, char, prop):
		self.char=char

		self.structure=prop[0]

		self._cangjie=None
		self._array=None
		self._dayi=None
		self._boshiamy=None
		self._boshiamy_supplement=None
		self._zhengma=None
		self._zhengma_type=None

		if len(prop)>=8:
			self.setIMproperty(prop)

	def __str__(self):
		return self.char

	def __repr__(self):
		return str(self)

	def setIMproperty(self, prop):
		self.cj=prop[1]
		self.ar=prop[2]
		self.dy=prop[3]
		self.bs, self.bssp=prop[4], prop[5]
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
	def bscode(self):
		if self.bs==None or self.bssp==None:
			return None
		if len(self.bs)<3:
			return self.bs+self.bssp
		else:
			return self.bs

	@property
	def bs(self):
		if self._boshiamy==None:
			return None
		return self._boshiamy

	@bs.setter
	def bs(self, code):
		if code=='XXXX':
			self._boshiamy=None
		else:
			self._boshiamy=code

	@property
	def bssp(self):
		if self._boshiamy_supplement==None:
			return None
		return self._boshiamy_supplement

	@bssp.setter
	def bssp(self, sp):
		if sp=='XXXX':
			self._boshiamy_supplement=None
		else:
			self._boshiamy_supplement=sp

	@property
	def zm(self):
		if self._zhengma==None or self._zhengma_type==None:
			return None
		return self._zhengma

	@zm.setter
	def zm(self, code):
		if code[0]=='XXXX' or code[1]=='XXXX':
			self._zhengma=None
			self.zmtp=None
		else:
			self._zhengma=code[0]
			self.zmtp=code[1]

	@property
	def zmtp(self):
		return self._zhengma_type

	@zmtp.setter
	def zmtp(self, type):
		self._zhengma_type=type

if __name__=='__main__':
	c=Char('王', ['(龜)', 'hn', 'sl', '/c', 'k', 'l', 'qy', '12'])
	print('倉頡', c.cj)
	print('行列', c.ar)
	print('大易', c.dy)
	print('嘸蝦米', c.bs, c.bssp)
	print('鄭碼', c.zm, c.zmtp)

