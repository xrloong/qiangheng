from im import IM
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
	def getIMModule(imName):
		if imName == '倉頡':
			imModule=CangJie
		elif imName == '行列':
			imModule=Array
		elif imName == '大易':
			imModule=DaYi
		elif imName == '嘸蝦米':
			imModule=Boshiamy
		elif imName == '鄭碼':
			imModule=ZhengMa
		else:
			imModule=IM

		return imModule

	@staticmethod
	def getIM(imName):
		imModule=IMMgr.getIMModule(imName)
		return imModule.IMInfo

	@staticmethod
	def getCharInfoGenerator(imName):
		imModule=IMMgr.getIMModule(imName)
		return imModule.CharInfoGenerator

if __name__=='__main__':
	pass

