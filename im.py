
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
				code=ch.getCode()
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

	def setCharInfoOfCharDesc(self, chdesc):
		# 多型
		descList=self.normalizationToLinear(chdesc)
		complist=[x.getChInfo() for x in descList]

		charinfo=chdesc.getChInfo()
		charinfo.setByComps(complist)

	def setCharTree(self, chdesc):
		"""設定某一個字符所包含的部件的碼"""

		if not chdesc.getChInfo().isToSetTree():
			return

		expand_chdesc=chdesc.expandCharTree(self.descDB)
		descList=self.normalizationToLinear(expand_chdesc)
		for tmpdesc in descList:
			self.setCharTree(tmpdesc)

		self.setCharInfoOfCharDesc(expand_chdesc)

	def normalizationToLinear(self, comp):
		"""將樹狀結構轉為線性結構"""
		# 多型
		if len(comp.getCompList())==0:
			return [comp]
		return sum(map(lambda x: self.normalizationToLinear(x), comp.getCompList()), [])

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

	def setCharInfoOfCharDesc(self, chdesc):
		prelist, postlist=self.getCJPrePostList(chdesc)

		pre_chinfo_list=map(lambda x:x.getChInfo(), prelist)
		post_chinfo_list=map(lambda x:x.getChInfo(), postlist)

		charinfo=chdesc.getChInfo()
		charinfo.setCJByComps(pre_chinfo_list, post_chinfo_list)

	def normalizationToLinear(self, chdesc):
		"""將樹狀結構轉為線性結構"""
		return chdesc.getCompList()

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

if __name__=='__main__':
	pass

