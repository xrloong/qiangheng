from .IMInfo import IMInfo
from .IMInfo import ArrayInfo
from .IMInfo import BoshiamyInfo
from .IMInfo import CangJieInfo
from .IMInfo import DaYiInfo
from .IMInfo import ZhengMaInfo

from .CodeInfo import CodeInfo
from .CodeInfo import ARCodeInfo
from .CodeInfo import BSCodeInfo
from .CodeInfo import CJCodeInfo
from .CodeInfo import DYCodeInfo
from .CodeInfo import ZMCodeInfo

class IMMgr:
	def __init__(self):
		pass

	@staticmethod
	def getIMModule(imName):
		if imName == '倉頡':
			imModule=CangJieInfo
		elif imName == '行列':
			imModule=ArrayInfo
		elif imName == '大易':
			imModule=DaYiInfo
		elif imName == '嘸蝦米':
			imModule=BoshiamyInfo
		elif imName == '鄭碼':
			imModule=ZhengMaInfo
		else:
			imModule=IMInfo

		return imModule

	@staticmethod
	def getIM(imName):
		imModule=IMMgr.getIMModule(imName)
		return imModule.IMInfo

	@staticmethod
	def getCodeInfoGenerator(imName):
		imModule=IMMgr.getIMModule(imName)
		return imModule.CodeInfoGenerator

if __name__=='__main__':
	pass

