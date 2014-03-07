from .CJCodeInfo import CJCodeInfo
from .CJCodeInfo import GridCJCodeInfo
from .CJLump import CJLump
from ..base.CodeInfoEncoder import CodeInfoEncoder
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
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		direction='*'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
		direction='$'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		direction='*'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		direction='|'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		direction='-'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		direction='@'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsMu(cls, codeInfoList):
		direction='$'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		direction='$'
		codeInfoList=CJCodeInfoEncoder.convertCodeInfoListOfZuoOrder(codeInfoList)
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		direction='$'
		cjLumpList=CJCodeInfoEncoder.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=cls.generateDefaultCodeInfo(direction, cjLumpList)
		return codeInfo


	@classmethod
	def encodeAsLin(cls, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=CJCodeInfoEncoder.encodeAsLoong([firstCodeInfo])
		bottomCodeInfo=cls.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=cls.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	@classmethod
	def encodeAsYi(cls, codeInfoList):
		"""運算 "燚" """
		firstCodeInfo=codeInfoList[0]

		tmpCodeInfoH=cls.encodeAsGoose([firstCodeInfo, firstCodeInfo])
		codeInfoV=cls.encodeAsSilkworm([tmpCodeInfoH, tmpCodeInfoH])

		tmpCodeInfoV=cls.encodeAsSilkworm([firstCodeInfo, firstCodeInfo])
		codeInfoH=cls.encodeAsGoose([tmpCodeInfoV, tmpCodeInfoV])

		codeInfo=GridCJCodeInfo(codeInfoV, codeInfoH)

		return codeInfo

	@staticmethod
	def computeLumpListInDirection(direction, codeInfo):
		tmpDirCode=codeInfo.getDirection()

		if direction=='$':
			lumpList=codeInfo.getLumpList()
		elif tmpDirCode in ['@']:
			tmpRadixList=codeInfo.getLumpList()
			tmpCJLump=CJLump.generateContainer(tmpRadixList)
			lumpList=[tmpCJLump]
		elif tmpDirCode in ['*']:
			tmpRadixList=codeInfo.getLumpList()
			tmpCJLump=CJLump.generateBody(tmpRadixList)
			lumpList=[tmpCJLump]
		elif tmpDirCode in ['+'] and isinstance(codeInfo, GridCJCodeInfo):
			if direction=='-':
				newCodeInfo=codeInfo.getCodeInfoH()
				lumpList=newCodeInfo.getLumpList()
			elif direction=='|':
				newCodeInfo=codeInfo.getCodeInfoV()
				lumpList=newCodeInfo.getLumpList()
			else:
				ci=codeInfo.getCodeInfoV()
				tmpCJLump=CJLump.generateBody(ci.getLumpList())
				lumpList=[tmpCJLump]
		else:
			if tmpDirCode==direction:
				# 同向
				lumpList=codeInfo.getLumpList()
			else:
				# 不同向
				tmpRadixList=codeInfo.getLumpList()
				tmpCJLump=CJLump.generateBody(tmpRadixList)
				lumpList=[tmpCJLump]
		return lumpList

	@staticmethod
	def convertCodeInfoListToRadixList(direction, codeInfoList):
		ansLumpList=[]
		for tmpCodeInfo in codeInfoList:
			tmpRadixList=CJCodeInfoEncoder.computeLumpListInDirection(direction, tmpCodeInfo)
			ansLumpList.extend(tmpRadixList)
		return ansLumpList

