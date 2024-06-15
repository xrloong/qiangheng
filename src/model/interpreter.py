from injector import inject

from element.operator import Operator

from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder

class CodeInfoInterpreter:
	@inject
	def __init__(self, codeInfoEncoder: CodeInfoEncoder):
		self.__codeInfoEncoder = codeInfoEncoder

	def __interpretCodeInfo(self, codeInfo: CodeInfo) -> str:
		return codeInfo.code

	def encodeToCodeInfo(self, operator: Operator, codeInfoList: list[CodeInfo]) -> CodeInfo:
		codeInfo = self.__codeInfoEncoder.setByComps(operator, codeInfoList)
		if codeInfo != None:
			for childCodeInfo in codeInfoList:
				codeVariance = childCodeInfo.getCodeVariance()
				codeInfo.multiplyCodeVariance(codeVariance)
		return codeInfo

	def interpretCodeInfoList(self, codeInfoList: list[CodeInfo]) -> list[(str, str)]:
		codeList = []
		for codeInfo in codeInfoList:
			characterCode = self.__interpretCodeInfo(codeInfo)
			variance = codeInfo.variance
			if characterCode:
				codeList.append([characterCode, str(variance)])

		return codeList
