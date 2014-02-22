from .IMInfo import IMInfo
from .IMInfo import ArrayInfo
from .IMInfo import BoshiamyInfo
from .IMInfo import CangJieInfo
from .IMInfo import DaYiInfo
from .IMInfo import DynamicCompositionInfo
from .IMInfo import FourCornerInfo
from .IMInfo import GuiXieInfo
from .IMInfo import ZhengMaInfo
from .IMInfo import SampleInfo

class IMMgr:
	def __init__(self):
		pass

	@staticmethod
	def getIMModule(imProp):
		imName=imProp['名稱']

		if imName in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
			imName='倉頡'
		elif imName in ['行', '行列', '行列輸入法', 'array', 'ar',]:
			imName='行列'
		elif imName in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
			imName='大易'
		elif imName in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
			imName='嘸蝦米'
		elif imName in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
			imName='鄭碼'
		elif imName in ['動', '動組', '動態組字', 'dynamiccomposition', 'dc',]:
			imName='動組'
		elif imName in ['四', '四角', '四角號碼', 'fourcorner', 'fc',]:
			imName='四角'
		elif imName in ['庋', '庋㩪', '中國字庋㩪', 'guixie', 'gx',]:
			imName='庋㩪'
		elif imName in ['例', '範例', '範例輸入法', 'sample', 'sp',]:
			imName='範例'
		else:
			imName='空'

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
		elif imName == '動組':
			imModule=DynamicCompositionInfo
		elif imName == '四角':
			imModule=FourCornerInfo
		elif imName == '庋㩪':
			imModule=GuiXieInfo
		elif imName == '範例':
			imModule=SampleInfo
		else:
			imModule=IMInfo

		return imModule

if __name__=='__main__':
	pass

