from ..CodeInfo.ZMCodeInfo import ZMCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear import Operator

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=ZMCodeInfo(propDict, codeVariance)
		rtlist=codeInfo.getRtList()
		zmCode=self.computeCharacterCode(rtlist)
		codeInfo.setCharacterCode(zmCode)
		return codeInfo

	def isAvailableOperation(self, operator, codeInfoList):
		return all(codeInfoList)

	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """

		rtlist=sum(map(lambda c: c.getZMProp(), codeInfoList), [])
		if codeInfoList and all(rtlist):
			rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
			zmCode=self.computeCharacterCode(rtlist)
			if Operator.OperatorLiang.equals(operator):
				codeInfo.setZMProp(rtlist[:1])
			else:
				codeInfo.setZMProp(rtlist)
			codeInfo.setCharacterCode(zmCode)

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def computeCharacterCode(self, rtlist):
		ans=''
		tmp_rtlist=rtlist
		if len(tmp_rtlist)==0:
			return None
		elif len(tmp_rtlist)==1:
			ans=rtlist[0]
		elif len(tmp_rtlist)==2:
			if len(tmp_rtlist[0])==1 and len(tmp_rtlist[1])==1:
				ans=''.join(rtlist[0:2])
				ans=rtlist[0][0]+rtlist[-1][0]+'vv'
			else:
				ans=(rtlist[0]+rtlist[-1])[:4]
		elif len(tmp_rtlist)==3:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-1][0:2]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		elif len(tmp_rtlist)>=4:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		else:
			ans=''
		return ans

