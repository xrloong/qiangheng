
class NoneIM:
	"輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		return []

	def genCompList(self, ch, chdict):
		if ch.structure[1] in ['龜']:
			return [ch]
		elif ch.structure[1] in ['好', '志']:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			if x and y:
				return self.genCompList(x,  chdict)+self.genCompList(y, chdict)
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
			complist=self.genCompList(ch, chdict)
			arlist=list(map(lambda c: c.ar, complist))
			if complist and all(arlist):
				cat="".join(arlist)
				if len(cat)>4:
					ch.ar=(cat[:3]+cat[-1])
				else:
					ch.ar=(cat)
				table.append([ch.ar, chname])
		return table

class DaYi(NoneIM):
	"大易輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			complist=self.genCompList(ch, chdict)
			dylist=list(map(lambda c: c.dy, complist))
			if complist and all(dylist):
				cat="".join(dylist)
				if len(cat)>4:
					ch.dy=(cat[:3]+cat[-1])
				else:
					ch.dy=(cat)
				table.append([ch.dy, chname])
		return table

class Boshiamy(NoneIM):
	"嘸蝦米輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			complist=self.genCompList(ch, chdict)
			bslist=list(map(lambda c: c.bs, complist))
			if complist and all(bslist):
				cat="".join(bslist)
				if len(cat)>4:
					ch.bs=(cat[:3]+cat[-1])
				else:
					ch.bs=(cat)
				ch.bssp=complist[-1].bssp
				table.append([ch.bscode, chname])
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

if __name__=='__main__':
	pass

