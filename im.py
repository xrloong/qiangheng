
class NoneIM:
	"輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		return []

class CangJie(NoneIM):
	"倉頡輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			if ch.cj:
				table.append([ch.cj, chname])
		return table

class Array(NoneIM):
	"行列輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			if ch.ar:
				table.append([ch.ar, chname])
		return table

class DaYi(NoneIM):
	"大易輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			if ch.dy:
				table.append([ch.dy, chname])
		return table

class Boshiamy(NoneIM):
	"嘸蝦米輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			if ch.bs:
				table.append([ch.bs, chname])
		return table

class ZhengMa(NoneIM):
	"鄭碼輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			if ch.zm:
				table.append([ch.zm, chname])
		return table

