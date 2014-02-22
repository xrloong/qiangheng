from gear.CodeInfoEncoder import CodeInfoEncoder

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def setByComps(self, codeInfo, operator, codeInfoList):
		if all(codeInfoList):
			rtlist=sum(map(lambda c: c.getZMProp(), codeInfoList), [])
			if codeInfoList and all(rtlist):
				rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
				codeInfo.setZMProp(rtlist)

