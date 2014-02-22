from . import IM
from . import Array
from . import Boshiamy
from . import CangJie
from . import DaYi
from . import ZhengMa

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
	def getCodeInfoGenerator(imName):
		imModule=IMMgr.getIMModule(imName)
		return imModule.CodeInfoGenerator

if __name__=='__main__':
	pass

