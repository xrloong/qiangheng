
class NoneIM:
	"輸入法"

	def __init__(self):
		self.keyMaps=[]

	def setTable(self, tb):
		self.tb=tb
		self.method='T'

	def setStruct(self, chdict):
		self.chdict=chdict
		self.method='D'

	def genIMMapping(self):
		if self.method=='D':
			table=[]
			for chname, ch in self.chdict.items():
				self.setCharTree(ch)
				code=self.getCode(ch)
				if code:
					table.append([code, chname])
				else:
					pass
#					print("Debug", chname)
		elif self.method=='T':
			table=self.tb
		else:
			table=[]
		return table

	def getCode(self, ch):
		pass

	def setCharTree(self, ch):
		pass

	def getAllComp(self, ch):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		chdict=self.chdict
		if ch.structure[1] in ['龜']:
			return []
		elif ch.structure[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			return [x, y]
		elif ch.structure[1] in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			z=chdict.get(ch.structure[5], None)
			return [x, y, z]
		elif ch.structure[1] in ['纂',]:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			z=chdict.get(ch.structure[5], None)
			w=chdict.get(ch.structure[6], None)
			return [x, y, z, w]
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
		self.keyMaps=[
			['a', '日',],
			['b', '月',],
			['c', '金',],
			['d', '木',],
			['e', '水',],
			['f', '火',],
			['g', '土',],
			['h', '竹',],
			['i', '戈',],
			['j', '十',],
			['k', '大',],
			['l', '中',],
			['m', '一',],
			['n', '弓',],
			['o', '人',],
			['p', '心',],
			['q', '手',],
			['r', '口',],
			['s', '尸',],
			['t', '廿',],
			['u', '山',],
			['v', '女',],
			['w', '田',],
			['x', '難',],
			['y', '卜',],
			['z', '符',],
			]

	def getCode(self, ch):
		if ch.cj:
			return ch.cj

	def getCJPrePostList(self, ch):
		"""傳回倉頡的字首及字尾的部件串列"""
		chdict=self.chdict
		prelist=[]
		postlist=[]
		if ch.structure[1] in ['龜']:
			prelist=[]
			postlist=[]
		elif ch.structure[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起']:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			prelist=[x]
			postlist=[y]
		elif ch.structure[1] in ['算', '湘', '霜', '怡',]:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			z=chdict.get(ch.structure[5], None)
			prelist=[x]
			postlist=[y, z]
		elif ch.structure[1] in ['想', '穎',]:
			x=chdict.get(ch.structure[3], None)
			y=chdict.get(ch.structure[4], None)
			z=chdict.get(ch.structure[5], None)
			prelist=[x, y]
			postlist=[z]
		elif ch.structure[1] in ['林', '爻']:
			x=chdict.get(ch.structure[3], None)
			prelist=[x]
			postlist=[x]
		elif ch.structure[1] in ['卅', '鑫']:
			x=chdict.get(ch.structure[3], None)
			prelist=[x]
			postlist=[x, x]
		elif ch.structure[1] in ['燚',]:
			x=chdict.get(ch.structure[3], None)
			prelist=[x, x]
			postlist=[x, x]
		else:
			prelist=[]
			postlist=[]
		return [prelist, postlist]

	def setCharTree(self, ch):
		"""設定某一個字符所包含的部件的碼"""

		if ch.cj:
			# 如果有值，代表事先指定或之前設定過。
			return

		def getCJPrefixCode(prelist):
			"""計算倉頡字首的碼"""

			# 字首最多取兩碼
			if len(prelist)==1:
				# 如果字首只有一個部件
				tmpcode=prelist[0].cj
				if len(tmpcode)<=2:
					# 字首小於或剛好二個碼就全取
					return tmpcode
				else:
					# 字首有超過二個碼就首碼及尾碼
					return tmpcode[0]+tmpcode[-1]
			else:
				# 如果字首有超過一個部件，則取首部件的首碼及尾部件的尾碼
				return prelist[0].cj[0]+prelist[-1].cj[-1]

		def getCJPostfixCode(postlist):
			"""計算倉頡字身的碼"""

			# 字身最多取三碼
			if len(postlist)==1:
				# 如果字身只有一個部件
				tmpcode=postlist[0].cj
				if len(tmpcode)<=3:
					# 字身只有三個碼就全取
					return tmpcode
				else:
					# 字身有超過三個碼就首碼、次碼及尾碼
					return tmpcode[0:2]+tmpcode[-1]
			else:
				# 如果字身有超過一個部件
				tmpcode=postlist[0].cj
				if len(tmpcode)==1:
					# 如果次字首有只有一個碼
					# 則取次字首的全碼及次字身的尾碼及尾碼
					return tmpcode+getCJPrefixCode(postlist[1:])
				else:
					# 如果次字首有有超過一個碼
					# 則取次字首的首碼及尾碼及最後部件的尾碼
					return tmpcode[0]+tmpcode[-1]+postlist[-1].cj[-1]

		[prefixlist, postfixlist]=self.getCJPrePostList(ch)

		tmplist=prefixlist+postfixlist
		for tmpch in tmplist:
			self.setCharTree(tmpch)

		if prefixlist and postfixlist and all(tmplist) and all(map(lambda ch: ch.cj, tmplist)):
			cjcode=getCJPrefixCode(prefixlist)+getCJPostfixCode(postfixlist)
			ch.cj=cjcode

class Array(NoneIM):
	"行列輸入法"

	def __init__(self):
		self.keyMaps=[
			['a', '1-',],
			['b', '5v',],
			['c', '3v',],
			['d', '3-',],
			['e', '3^',],
			['f', '4-',],
			['g', '5-',],
			['h', '6-',],
			['i', '8^',],
			['j', '7-',],
			['k', '8-',],
			['l', '9-',],
			['m', '7v',],
			['n', '6v',],
			['o', '9^',],
			['p', '0^',],
			['q', '1^',],
			['r', '4^',],
			['s', '2-',],
			['t', '5^',],
			['u', '7^',],
			['v', '4v',],
			['w', '2^',],
			['x', '2v',],
			['y', '6^',],
			['z', '1v',],
			['.', '9v',],
			['/', '0v',],
			[';', '0-',],
			[',', '8v',],
			['1', '１',],
			['2', '２',],
			['3', '３',],
			['4', '４',],
			['5', '５',],
			['6', '６',],
			['7', '７',],
			['8', '８',],
			['9', '９',],
			['0', '０',],
			]

	def getCode(self, ch):
		if ch.ar:
			return ch.ar

	def setCharTree(self, ch):
		if ch.ar:
			return

		complist=self.getAllComp(ch)

		for tmpch in complist:
			self.setCharTree(tmpch)

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
		self.keyMaps=[
			[',', '力',],
			['.', '點',],
			['/', '竹',],
			['0', '金',],
			['1', '言',],
			['2', '牛',],
			['3', '目',],
			['4', '四',],
			['5', '王',],
			['6', '門',],
			['7', '田',],
			['8', '米',],
			['9', '足',],
			[';', '虫',],
			['A', '人',],
			['B', '馬',],
			['C', '七',],
			['D', '日',],
			['E', '一',],
			['F', '土',],
			['G', '手',],
			['H', '鳥',],
			['I', '木',],
			['J', '月',],
			['K', '立',],
			['L', '女',],
			['M', '雨',],
			['N', '魚',],
			['O', '口',],
			['P', '耳',],
			['Q', '石',],
			['R', '工',],
			['S', '革',],
			['T', '糸',],
			['U', '艸',],
			['V', '禾',],
			['W', '山',],
			['X', '水',],
			['Y', '火',],
			['Z', '心',],
			]

	def getCode(self, ch):
		if ch.dy:
			return ch.dy

	def setCharTree(self, ch):
		if ch.dy:
			return

		complist=self.getAllComp(ch)

		for tmpch in complist:
			self.setCharTree(tmpch)

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
		self.keyMaps=[
			['a', 'Ａ',],
			['b', 'Ｂ',],
			['c', 'Ｃ',],
			['d', 'Ｄ',],
			['e', 'Ｅ',],
			['f', 'Ｆ',],
			['g', 'Ｇ',],
			['h', 'Ｈ',],
			['i', 'Ｉ',],
			['j', 'Ｊ',],
			['k', 'Ｋ',],
			['l', 'Ｌ',],
			['m', 'Ｍ',],
			['n', 'Ｎ',],
			['o', 'Ｏ',],
			['p', 'Ｐ',],
			['q', 'Ｑ',],
			['r', 'Ｒ',],
			['s', 'Ｓ',],
			['t', 'Ｔ',],
			['u', 'Ｕ',],
			['v', 'Ｖ',],
			['w', 'Ｗ',],
			['x', 'Ｘ',],
			['y', 'Ｙ',],
			['z', 'Ｚ',],
			]

	def getCode(self, ch):
		if ch.bscode:
			return ch.bscode

	def setCharTree(self, ch):
		if ch.bs:
			return

		complist=self.getAllComp(ch)

		for tmpch in complist:
			self.setCharTree(tmpch)

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
		self.keyMaps=[
			['a', 'Ａ',],
			['b', 'Ｂ',],
			['c', 'Ｃ',],
			['d', 'Ｄ',],
			['e', 'Ｅ',],
			['f', 'Ｆ',],
			['g', 'Ｇ',],
			['h', 'Ｈ',],
			['i', 'Ｉ',],
			['j', 'Ｊ',],
			['k', 'Ｋ',],
			['l', 'Ｌ',],
			['m', 'Ｍ',],
			['n', 'Ｎ',],
			['o', 'Ｏ',],
			['p', 'Ｐ',],
			['q', 'Ｑ',],
			['r', 'Ｒ',],
			['s', 'Ｓ',],
			['t', 'Ｔ',],
			['u', 'Ｕ',],
			['v', 'Ｖ',],
			['w', 'Ｗ',],
			['x', 'Ｘ',],
			['y', 'Ｙ',],
			['z', 'Ｚ',],
			]


	def getCode(self, ch):
		if ch.zm:
			return ch.zm

	def setCharTree(self, ch):
		if ch.zm:
			return

		complist=self.getAllComp(ch)

		for tmpch in complist:
			self.setCharTree(tmpch)

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
				elif type[1]=='3':
					return [[code[0:3], type], [code[3:], type]]
			elif type[0]=='3':
				if type[1]=='1':
					return [[code[0], type], [code[1], type], [code[2:], type]]
				elif type[1]=='2':
					return [[code[0:2], type], [code[2], type], [code[3], type]]
				elif type[1]=='3':
					return [[code[0:3], type], [code[3], type]]
			elif type[0]=='4':
				if type[1]=='1':
					return [[code[0], type], [code[1], type], [code[2], type], [code[3], type]]
				elif type[1]=='2':
					return [[code[0:2], type], [code[2], type], [code[3], type]]
				elif type[1]=='3':
					return [[code[0:3], type], [code[3], type]]

		def listToCode(l):
			nmCompList=sum(map(lambda x: int(x[1][0]), l))
			if nmCompList==1:
				# 如果部件數為 1
				# 鄭碼為首部件的全碼
				return [l[0][0], '1'+l[0][1][1]]
			elif nmCompList==2:
				# 如果部件數為 2
				# 鄭碼為首部件及尾部件的全碼
				if l[0][1][1]=='1':
					return [l[0][0][0:2]+l[-1][0][0:3], '21']
				elif l[0][1][1]=='2':
					return [l[0][0][0:2]+l[-1][0][0:2], '22']
				elif l[0][1][1]=='3':
					return [l[0][0][0:3]+l[-1][0][0:1], '23']
#				return [l[0][0]+l[1][0], '2'+l[0][1][1]]
			elif nmCompList==3:
				# 如果部件數為 3
				if l[0][1][1]=='1':
					# 如果首部件為單碼
					# 鄭碼為首部件的首碼，次末部件的首碼及尾部件的雙碼
					return [l[0][0][0]+l[-2][0][0]+l[-1][0][0:2], '31']
				elif l[0][1][1]=='2':
					# 如果首部件為雙碼
					# 鄭碼為首部件的雙碼，次末部件的首碼及尾部件的首碼
					return [l[0][0][0:2]+l[-2][0][0]+l[-1][0][0], '32']
				elif l[0][1][1]=='3':
					# 如果首部件為三碼
					# 鄭碼為首部件的雙碼，次末部件的首碼及尾部件的首碼
					return [l[0][0][0:3]+l[-1][0][0], '33']
			elif nmCompList>=4:
				# 如果部件數超過 4
				if l[0][1][1]=='1':
					# 如果首部件為單碼
					# 鄭碼為首部件的首碼、次首部件的首碼、次末部件的首碼及尾部件的雙碼
					return [l[0][0][0]+l[1][0][0]+l[-2][0][0]+l[-1][0][0], '41']
				elif l[0][1][1]=='2':
					# 如果首部件為雙碼
					# 鄭碼為首部件的雙碼，次末部件的首碼及尾部件的首碼
					return [l[0][0][0:2]+l[-2][0][0]+l[-1][0][0], '42']
				else:
					# 如果首部件為三碼
					return [l[0][0][0:3]+l[-1][0][0], '43']

		if all(complist):
			ctlist=list(map(lambda c: codeToList(c.zm, c.zmtp), complist))
			if complist and all(ctlist):
				code, type=listToCode(sum(ctlist, []))
				ch.zm=code
				ch.zmtp=type

if __name__=='__main__':
	pass

