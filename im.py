
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

	def getCode(self, ch):
		if ch.cj:
			return ch.cj

	def setCharTree(self, ch, chdict):
		if ch.ar:
			return

		complist=self.getAllComp(ch, chdict)

		for tmpch in complist:
			self.setCharTree(tmpch, chdict)

		def getLstcode(chlist):
			return chlist[-1].cj[-1]

		def getFstLstcode(chlist):
			if len(chlist)==1:
				cjcode=chlist[0].cj
				if len(cjcode)==1:
					return cjcode[0]
				elif len(cjcode)>=2:
					return cjcode[0]+cjcode[-1]
			elif len(chlist)>=2:
				return chlist[0].cj[0]+chlist[-1].cj[-1]

		def getFstSndLstcode(chlist):
			if len(chlist)==1:
				cjcode=chlist[0].cj
				if len(cjcode)<=2:
					return cjcode
				elif len(cjcode)>=3:
					return cjcode[0:2]+cjcode[-1]
			elif len(chlist)>=2:
				flcode=getFstLstcode(chlist)
				if len(flcode)==1:
					return flcode+getFstLstcode(chlist[1:])
				else:
					return flcode+getLstcode(chlist[1:])
		cjlist=list(map(lambda c: c.cj, complist))

		if complist and all(cjlist):
			if ch.structure[1] in ['龜']:
				cjcode=ch.cj
			elif ch.structure[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起']:
				x=chdict.get(ch.structure[3], None)
				y=chdict.get(ch.structure[4], None)
				cjcode=getFstLstcode([x])+getFstSndLstcode([y])
			elif ch.structure[1] in ['算', '湘', '霜', '想', '怡', '穎',]:
				x=chdict.get(ch.structure[3], None)
				y=chdict.get(ch.structure[4], None)
				z=chdict.get(ch.structure[5], None)
				cjcode=getFstLstcode([x])+getFstSndLstcode([y, z])
			elif ch.structure[1] in ['林', '爻']:
				x=chdict.get(ch.structure[3], None)
				cjcode=getFstLstcode([x])+getFstSndLstcode([x])
			elif ch.structure[1] in ['卅', '鑫']:
				x=chdict.get(ch.structure[3], None)
				cjcode=getFstLstcode([x])+getFstSndLstcode([x, x, x])
			elif ch.structure[1] in ['燚',]:
				x=chdict.get(ch.structure[3], None)
				cjcode=getFstLstcode([x, x])+getFstSndLstcode([x, x])
			else:
				cjcode=""
			if cjcode:
				ch.cj=cjcode

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

	def getCode(self, ch):
		if ch.zm:
			return ch.zm

	def setCharTree(self, ch, chdict):
		if ch.zm:
			return

		complist=self.getAllComp(ch, chdict)

		for tmpch in complist:
			self.setCharTree(tmpch, chdict)

		def codeToList(code, type):
			if not code or not type:
				return None
			if type[0]=='1':
				return [[code, type]]
			elif type[0]=='2':
				if type[1]=='1':
					return [[code[0], type], [code[1:], type]]
				elif type[1]=='2':
					return [[code[0:2], type], [code[2:], type]]
			elif type[0]=='3':
				if type[1]=='1':
					return [[code[0], type], [code[1], type], [code[2:], type]]
				elif type[1]=='2':
					return [[code[0:2], type], [code[2], type], [code[3], type]]
			elif type[0]=='4':
				if type[1]=='1':
					return [[code[0], type], [code[1], type], [code[2], type], [code[3], type]]
				elif type[1]=='2':
					return [[code[0:2], type], [code[2], type], [code[3], type]]

		def listToCode(l):
			nmCompList=sum(map(lambda x: int(x[1][0]), l))
			if nmCompList==1:
				return [l[0][0], '1'+l[0][1][1]]
			elif nmCompList==2:
				return [l[0][0]+l[1][0], '2'+l[0][1][1]]
			elif nmCompList==3:
				if l[0][1][1]=='1':
					return [l[0][0][0]+l[-2][0][0]+l[-1][0][0:2], '3'+l[0][1][1]]
				else:
					return [l[0][0][0:2]+l[-2][0][0]+l[-1][0][0], '3'+l[0][1][1]]
			elif nmCompList>=4:
				if l[0][1][1]=='1':
					return [l[0][0][0]+l[1][0][0]+l[-2][0][0]+l[-1][0][0], '4'+l[0][1][1]]
				else:
					return [l[0][0][0:2]+l[-2][0][0]+l[-1][0][0], '4'+l[0][1][1]]

		if all(complist):
			ctlist=list(map(lambda c: codeToList(c.zm, c.zmtp), complist))
			if complist and all(ctlist):
				code, type=listToCode(sum(ctlist, []))
				ch.zm=code
				ch.zmtp=type

if __name__=='__main__':
	pass

