from ..CodeInfo.CJCodeInfo import CJCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear.CodeInfo import CodeInfo

class CJCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, direction, ansRadixList):
		return CJCodeInfo.generateDefaultCodeInfo(direction, ansRadixList)

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=CJCodeInfo.generateCodeInfo(propDict)
		codeInfo.multiplyCodeVarianceType(codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		direction='*'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo


	def encodeAsSilkworm(self, codeInfoList):
		direction='|'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		direction='-'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		direction='@'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo


	def encodeAsMu(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		direction='$'
		ansRadixList=self.convertCodeInfoListToRadixList(direction, codeInfoList)
		codeInfo=self.generateDefaultCodeInfo(direction, ansRadixList)
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
		ansRadixList=[]
		for tmpCodeInfo in codeInfoList:
			tmpDirCode=tmpCodeInfo.getDirection()
			tmpRadixList=tmpCodeInfo.getRtList()
			if direction=='$':
				ansRadixList.extend(tmpRadixList)
			elif tmpDirCode in ['*', '@']:
				ansRadixList.append(tmpCodeInfo.getBodyCode())
			elif tmpDirCode==direction:
				# 同向
				ansRadixList.extend(tmpRadixList)
			else:
				# 不同向
				ansRadixList.append(tmpCodeInfo.getBodyCode())

		return ansRadixList

	def encodeAsYin(self, codeInfoList):
		"""運算 "胤" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		if firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_儿:
			radix_丨=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_丨])

			radix_乚=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_乚])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_乚])
			return codeInfo
#		elif firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_丨 and firstCodeInfo.getRtList()[1]==CJCodeInfo.RADIX_丨:
#		elif firstCodeInfo.getRtList()[0]==CJCodeInfo.RADIX_丨丨:
		elif firstCodeInfo.getRtList()[0]=="l" and firstCodeInfo.getRtList()[1]=="l":
			# work around
			radix_丨=self.generateDefaultCodeInfo('*', [CJCodeInfo.RADIX_丨])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_丨])
			return codeInfo
		else:
			return self.encodeAsInvalidate(codeInfoList)


