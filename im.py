
import copy
from charinfo import *
from chardesc import *

class NoneIM:
	"輸入法"

	def __init__(self):
		self.keyMaps=[]
		self.nameDict={
				'cn':'空',
				'tw':'空',
				'hk':'空',
				'en':'None',
				}
		self.iconfile="empty.png"
		self.maxkeylength=0

	def getName(self, localization):
		return self.nameDict.get(localization, "")

	def getIconFileName(self):
		return self.iconfile

	def getMaxKeyLength(self):
		return self.maxkeylength

	def getKeyList(self):
		return "".join(list(zip(*self.keyMaps))[0])

	def setTable(self, tb):
		self.tb=tb
		self.method='T'

	def setStruct(self, descDB):
		self.descDB=descDB
		self.method='D'

	def genIMMapping(self):
		def getSmallDescDB():
			charlist=[
					'土',
					'吉',
					'夠',
					'炎',
					'畦',
					]
			smallDB={}
			for chname in charlist:
				chdesc=self.descDB.get(chname, None)
				if chdesc:
					smallDB[chname]=chdesc

			return smallDB

		if self.method=='D':
			targetDB=self.descDB
#			targetDB=getSmallDescDB()

			table=[]
			for chname, chdesc in targetDB.items():
				self.setCharTree(chdesc)

				ch=chdesc.getChInfo()
				code=self.getCode(ch)
				if ch.isToShow() and code:
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
		ch=chdesc.getChInfo()

	def getCorespondingChInfo(self, charname, parseans, prop):
		return CharInfo(charname, parseans, prop)

	def setCharTree(self, chdesc):
		if not chdesc.getChInfo().isToSetTree():
			return

		expand_chdesc=self.expandCharTree(chdesc)
		descList=self.normalizationToLinear(expand_chdesc)
		for tmpdesc in descList:
			self.setCharTree(tmpdesc)

		complist=[x.getChInfo() for x in descList]

		charinfo=chdesc.getChInfo()
		charinfo.setByComps(complist)

	def expandCharTree(self, comp):

		if len(comp.getCompList())==0:
			chdesc=self.descDB.get(comp.name, None)
			if len(chdesc.getCompList())==0:
				return chdesc
			else:
				# 現有的資料已見底，但從 DB 中查到者仍可擴展
				return self.expandCharTree(chdesc)

		l=[]
		for tc in comp.getCompList():
			x=self.expandCharTree(tc)
			l.append(x)

		anscomp=self.getRearrangedDesc(comp)

		return anscomp

	def normalizationToLinear(self, comp):
		"""將樹狀結構轉為線性結構"""
		if len(comp.getCompList())==0:
			return [comp]
		return sum(map(lambda x: self.normalizationToLinear(x), comp.getCompList()), [])

	def normalizationToTree(self, comp):
		"""將樹狀結構轉為樹狀結構，目前即為不處理，提供一個介面。"""
		return comp

	def getRearrangedDesc(self, chdesc):
		[newOp, newCompList]=self.getRearrangedOpAndCompList(chdesc)
		chdesc.setOp(newOp)
		chdesc.setCompList(newCompList)
		return chdesc

	def getRearrangedOpAndCompList(self, chdesc):
#		['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
#		['好', '志',
#		'回', '同', '函', '區', '左',
#		'起', '廖', '載', '聖', '句',
#		'夾', '衍', '衷',]
#		['纂', '膷',]
		descDB=self.descDB
		ch=chdesc.getChInfo()

		newOperator='龜'
		newCompList=[]

		oldOperator=ch.operator
		oldCompList=[x for x in map(lambda x: x.name, chdesc.getCompList())]

		if oldOperator in ['龜']:
			newOperator=oldOperator
			newCompList=[]
		elif oldOperator in ['水']:
			x=descDB.get(oldCompList, None)
			x=oldCompList[0]

			newOperator=oldOperator
			newCompList=[x]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)

			newOperator=oldOperator
			newCompList=[x, y]
		elif oldOperator in ['算', '湘', '霜', '想', '怡', '穎',]:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)
			z=descDB.get(oldCompList[2], None)

			newOperator=oldOperator
			newCompList=[x, y, z]
		elif oldOperator in ['纂',]:
			x=descDB.get(oldCompList[0], None)
			y=descDB.get(oldCompList[1], None)
			z=descDB.get(oldCompList[2], None)
			w=descDB.get(oldCompList[3], None)

			newOperator=oldOperator
			newCompList=[x, y, z, w]
		elif oldOperator in ['林', '爻']:
			x=descDB.get(oldCompList[0], None)

			if oldOperator=='林':
				newOperator='好'
			elif oldOperator=='爻':
				newOperator='志'
			else:
				newOperator='錯'
			newCompList=[x, x]
		elif oldOperator in ['卅', '鑫']:
			x=descDB.get(oldCompList[0], None)

			if oldOperator=='卅':
				newOperator='湘'
			elif oldOperator=='鑫':
				# 暫不處理
				newOperator='算'
			else:
				newOperator='錯'
			newCompList=[x, x, x]
		elif oldOperator in ['燚',]:
			# 暫不處理
			x=descDB.get(oldCompList[0], None)

			newOperator=oldOperator
			newCompList=[x, x, x, x]
		else:
			newOperator='龜'
			newCompList=[]
#		chdesc.setOp(newOperator)
#		chdesc.setCompList(newCompList)
		return [newOperator, newCompList]

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
		self.nameDict={
				'cn':'仓颉',
				'tw':'倉頡',
				'hk':'倉頡',
				'en':'CangJie',
				}
		self.iconfile="CangJie.png"
		self.maxkeylength=5

	def getCode(self, ch):
		if ch.cj:
			return ch.cj

	def getCorespondingChInfo(self, charname, parseans, prop):
		return CJCharInfo(charname, parseans, prop)

	def getCJPrePostList(self, chdesc):
		"""傳回倉頡的字首及字尾的部件串列"""

		descDB=self.descDB
		oldOperator=chdesc.op
		oldCompList=chdesc.getCompList()

		prelist=[]
		postlist=[]
		if oldOperator in ['龜']:
			prelist=[]
			postlist=[]
		elif oldOperator in ['水']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[]
		elif oldOperator in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾']:
			x=oldCompList[0]
			y=oldCompList[1]
			prelist=[x]
			postlist=[y]
		elif oldOperator in ['算', '湘', '霜', '怡',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			prelist=[x]
			postlist=[y, z]
		elif oldOperator in ['想', '穎',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			prelist=[x, y]
			postlist=[z]
		elif oldOperator in ['林', '爻']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[x]
		elif oldOperator in ['卅', '鑫']:
			x=oldCompList[0]
			prelist=[x]
			postlist=[x, x]
		elif oldOperator in ['燚',]:
			x=oldCompList[0]
			prelist=[x, x]
			postlist=[x, x]
		elif oldOperator in ['纂',]:
			x=oldCompList[0]
			y=oldCompList[1]
			z=oldCompList[2]
			w=oldCompList[3]
			prelist=[x]
			postlist=[y, z, w]
		else:
			prelist=[]
			postlist=[]
		return [prelist, postlist]

	def setCharTree(self, chdesc):
		"""設定某一個字符所包含的部件的碼"""

		if not chdesc.getChInfo().isToSetTree():
			# 如果有值，代表事先指定或之前設定過。
			return

		expand_chdesc=self.expandCharTree(chdesc)
		descList=self.normalizationToLinear(expand_chdesc)
#		descList=self.normalizationToLinear(self.expandCharTree(chdesc))
		for tmpdesc in descList:
			self.setCharTree(tmpdesc)

		prelist, postlist=self.getCJPrePostList(expand_chdesc)
		for tmpchdesc in prelist+postlist:
			self.setCharTree(tmpchdesc)

		pre_chinfo_list=map(lambda x:x.getChInfo(), prelist)
		post_chinfo_list=map(lambda x:x.getChInfo(), postlist)

		charinfo=chdesc.getChInfo()
		charinfo.setCJByComps(pre_chinfo_list, post_chinfo_list)

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
			]
		self.nameDict={
				'cn':'行列',
				'tw':'行列',
				'hk':'行列',
				'en':'Array',
				}
		self.iconfile="Array.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.ar:
			return ch.ar

	def getCorespondingChInfo(self, charname, parseans, prop):
		return ARCharInfo(charname, parseans, prop)

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
		self.nameDict={
				'cn':'大易',
				'tw':'大易',
				'hk':'大易',
				'en':'DaYi',
				}
		self.iconfile="DaYi.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.dy:
			return ch.dy

	def getCorespondingChInfo(self, charname, parseans, prop):
		return DYCharInfo(charname, parseans, prop)

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
		self.nameDict={
				'cn':'呒蝦米',
				'tw':'嘸蝦米',
				'hk':'嘸蝦米',
				'en':'Boshiamy',
				}
		self.iconfile="Boshiamy.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.bs:
			return ch.bs

	def getCorespondingChInfo(self, charname, parseans, prop):
		return BSCharInfo(charname, parseans, prop)

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
		self.nameDict={
				'cn':'郑码',
				'tw':'鄭碼',
				'hk':'鄭碼',
				'nn':'Boshiamy',
				}
		self.iconfile="ZhengMa.png"
		self.maxkeylength=4

	def getCode(self, ch):
		if ch.zm:
			return ch.zm

	def getCorespondingChInfo(self, charname, parseans, prop):
		return ZMCharInfo(charname, parseans, prop)

if __name__=='__main__':
	pass

