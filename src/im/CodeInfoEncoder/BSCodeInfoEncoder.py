from ..CodeInfo.BSCodeInfo import BSCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class BSCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=BSCodeInfo(propDict, codeVariance)
		return codeInfo

	def setByComps(self, codeInfo, operator, codeInfoList):
		bslist=list(map(lambda c: c.getBSProp()[0], codeInfoList))
		if codeInfoList and all(bslist):
			cat="".join(bslist)
			bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
			bs_spcode=codeInfoList[-1].getBSProp()[1]
			codeInfo.setBSProp(bs_incode, bs_spcode)

