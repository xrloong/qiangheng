from im import NoneIM
from im import Array
from im import Boshiamy
from im import CangJie
from im import DaYi
from im import ZhengMa

from character import CharInfo
from character import ARCharInfo
from character import BSCharInfo
from character import CJCharInfo
from character import DYCharInfo
from character import ZMCharInfo

class IMMgr:
	def __init__(self):
		pass

	@staticmethod
	def getIM(imName):
		if imName == '倉頡':
			im=CangJie.CangJie()
		elif imName == '行列':
			im=Array.Array()
		elif imName == '大易':
			im=DaYi.DaYi()
		elif imName == '嘸蝦米':
			im=Boshiamy.Boshiamy()
		elif imName == '鄭碼':
			im=ZhengMa.ZhengMa()
		else:
			im=NoneIM.NoneIM()
		return im

	@staticmethod
	def getCharInfoGenerator(imName):
		if imName == '倉頡':
			cig=CJCharInfo.CJCharInfo
		elif imName == '行列':
			cig=ARCharInfo.ARCharInfo
		elif imName == '大易':
			cig=DYCharInfo.DYCharInfo
		elif imName == '嘸蝦米':
			cig=BSCharInfo.BSCharInfo
		elif imName == '鄭碼':
			cig=ZMCharInfo.ZMCharInfo
		else:
			cig=CharInfo.CharInfo
		return cig

if __name__=='__main__':
	pass

