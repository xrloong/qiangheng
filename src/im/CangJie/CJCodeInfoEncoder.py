from .CJCodeInfo import CJCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from .CJLump import CJLump
import sys

class CJCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, direction, cjLumpList):
		return CJCodeInfo.generateDefaultCodeInfo(direction, cjLumpList)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		return True


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		direction='*'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		direction='*'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsEast(cls, codeInfoList):
		"""運算 "雀" """
		direction='$'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		direction='*'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		direction='|'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		direction='-'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		direction='@'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsMu(cls, codeInfoList):
		direction='$'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		direction='$'
		codeInfoList=cls.convertCodeInfoListOfZuoOrder(codeInfoList)
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		direction='$'
		cjLumpList=cls.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsLin(cls, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=cls.encodeAsLoong([firstCodeInfo])
		bottomCodeInfo=cls.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=cls.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	@staticmethod
	def convertCodeInfoListToRadixList(direction, codeInfoList):
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

