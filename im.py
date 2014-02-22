
class NoneIM:
	"輸入法"

	def __init__(self):
		pass

	def genTable(self, chdict):
		table=[]
		for chname, ch in chdict.items():
			self.setCharTree(ch, chdict)
			code=self.getCode(ch)
			if code:
				table.append([code, chname])
		return table

	def getCode(self, ch):
		pass

	def setCharTree(self, ch, chdict):
		pass

	def genCompList(self, ch, chdict):
		if ch.structure[1] in ['龜']:
			return [ch]
		elif ch.structure[1] in ['好', '志']:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			if x and y:
				return self.genCompList(x,  chdict)+self.genCompList(y, chdict)
		return []

	def getAllComp(self, ch, chdict):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		if ch.structure[1] in ['龜']:
			return []
		elif ch.structure[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起']:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			return [x, y]
		elif ch.structure[1] in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			z=chdict.get(ch.structure[5], None)
			return [x, y, z]
		elif ch.structure[1] in ['林', '爻']:
			x=chdict.get(ch.structure[3], None)
			return [x, x]
		elif ch.structure[1] in ['卅', '鑫']:
			x=chdict.get(ch.structure[3], None)
			return [x, x, x]
		elif ch.structure[1] in ['燚',]:
			x=chdict.get(ch.structure[3], None)
			return [x, x, x, x]
		else:
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

	def getCode(self, ch):
		if ch.ar:
			return ch.ar

	def setCharTree(self, ch, chdict):
		if ch.ar:
			return

		complist=self.getAllComp(ch, chdict)

		for tmpch in complist:
			self.setCharTree(tmpch, chdict)

		arlist=list(map(lambda c: c.ar, complist))
		if complist and all(arlist):
			cat="".join(arlist)
			if len(cat)>4:
				ch.ar=(cat[:3]+cat[-1])
			else:
				ch.ar=(cat)


class DaYi(NoneIM):
	"大易輸入法"

	def __init__(self):
		pass

	def getCode(self, ch):
		if ch.dy:
			return ch.dy

	def setCharTree(self, ch, chdict):
		if ch.dy:
			return

		complist=self.getAllComp(ch, chdict)

		for tmpch in complist:
			self.setCharTree(tmpch, chdict)

		dylist=list(map(lambda c: c.dy, complist))
		if complist and all(dylist):
			cat="".join(dylist)
			if len(cat)>4:
				ch.dy=(cat[:3]+cat[-1])
			else:
				ch.dy=(cat)

class Boshiamy(NoneIM):
	"嘸蝦米輸入法"

	def __init__(self):
		pass

	def getCode(self, ch):
		if ch.bscode:
			return ch.bscode

	def setCharTree(self, ch, chdict):
		if ch.bs:
			return

		complist=self.getAllComp(ch, chdict)

		for tmpch in complist:
			self.setCharTree(tmpch, chdict)

		bslist=list(map(lambda c: c.bs, complist))
		if complist and all(bslist):
			cat="".join(bslist)
			if len(cat)>4:
				ch.bs=(cat[:3]+cat[-1])
			else:
				ch.bs=(cat)
			ch.bssp=complist[-1].bssp

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

