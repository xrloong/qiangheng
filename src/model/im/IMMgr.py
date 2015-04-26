class IMMgr:
	def __init__(self):
		pass

	@staticmethod
	def getIMPackage(imName):
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
		elif imName in ['筆順', 'strokeorder', 'so',]:
			imName='筆順'
		elif imName in ['四', '四角', '四角號碼', 'fourcorner', 'fc',]:
			imName='四角'
		elif imName in ['庋', '庋㩪', '中國字庋㩪', 'guixie', 'gx',]:
			imName='庋㩪'
		elif imName in ['例', '範例', '範例輸入法', 'sample', 'sample',]:
			imName='範例'
		else:
			imName='空'

		if imName == '倉頡':
			from . import CangJie
			imPackage=CangJie
		elif imName == '行列':
			from . import Array
			imPackage=Array
		elif imName == '大易':
			from . import DaYi
			imPackage=DaYi
		elif imName == '嘸蝦米':
			from . import Boshiamy
			imPackage=Boshiamy
		elif imName == '鄭碼':
			from . import ZhengMa
			imPackage=ZhengMa
		elif imName == '動組':
			from ..dm import DynamicComposition
			imPackage=DynamicComposition
		elif imName == '筆順':
			from . import StrokeOrder
			imPackage=StrokeOrder
		elif imName == '四角':
			from . import FourCorner
			imPackage=FourCorner
		elif imName == '庋㩪':
			from . import GuiXie
			imPackage=GuiXie
		elif imName == '範例':
			from . import Sample
			imPackage=Sample
		else:
			from . import base
			imPackage=base

		return imPackage

if __name__=='__main__':
	pass

