from .CJCodeInfo import CJCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from .CJLump import CJLump
import sys

class CJCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, direction, cjLumpList):
		return CJCodeInfo.generateDefaultCodeInfo(direction, cjLumpList)

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		direction='*'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		direction='*'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		direction='$'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		direction='*'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	def encodeAsSilkworm(self, codeInfoList):
		direction='|'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		direction='-'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		direction='@'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	def encodeAsMu(self, codeInfoList):
		direction='$'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		direction='$'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		direction='$'
		cjLumpList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	def encodeAsLin(self, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=self.encodeAsLoong([firstCodeInfo])
		bottomCodeInfo=self.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def convertCodeInfoListToRadixList(self, direction, codeInfoList):
		ansLumpList=[]
		for tmpCodeInfo in codeInfoList:
			tmpDirCode=tmpCodeInfo.getDirection()
			tmpRadixList=tmpCodeInfo.getLumpList()
			if direction=='$':
				ansLumpList.extend(tmpCodeInfo.getLumpList())
			elif tmpDirCode in ['@']:
				tmpCJLump=CJLump.generateContainer(tmpCodeInfo.getLumpList())
				ansLumpList.append(tmpCJLump)
			elif tmpDirCode in ['*']:
				tmpCJLump=CJLump.generateBody(tmpCodeInfo.getLumpList())
				ansLumpList.append(tmpCJLump)
			elif tmpDirCode==direction:
				# 同向
				ansLumpList.extend(tmpCodeInfo.getLumpList())
			else:
				# 不同向
				tmpCJLump=CJLump.generateBody(tmpCodeInfo.getLumpList())
				ansLumpList.append(tmpCJLump)
		return ansLumpList

	def encodeAsYin(self, codeInfoList):
		"""運算 "胤" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		if firstCodeInfo.getSpecialRadix()==CJCodeInfo.RADIX_儿:
			codeInfo=self.encodeAsGoose([CJCodeInfo.CODE_INFO_丨, secondCodeInfo, CJCodeInfo.CODE_INFO_乚])
			return codeInfo
		elif firstCodeInfo.getSpecialRadix()==CJCodeInfo.RADIX_丨丨:
			codeInfo=self.encodeAsGoose([CJCodeInfo.CODE_INFO_丨, secondCodeInfo, CJCodeInfo.CODE_INFO_丨])
			return codeInfo
		else:
			return self.encodeAsInvalidate(codeInfoList)


