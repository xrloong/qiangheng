from gear.CodeInfoEncoder import CodeInfoEncoder

class ARCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def setByComps(self, codeInfo, operator, codeInfoList):
		arlist=list(map(lambda c: c.getARProp(), codeInfoList))
		if codeInfoList and all(arlist):
			cat="".join(arlist)
			ar=cat[:3]+cat[-1] if len(cat)>4 else cat
			codeInfo.setARProp(ar)

