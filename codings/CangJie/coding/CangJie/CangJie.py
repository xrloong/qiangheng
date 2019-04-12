from coding.Base import CodingInfo
from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

import re

class CangJieInfo(CodingInfo):
	"倉頡輸入法"

	IMName="倉頡"
	def __init__(self):
		self.keyMaps=[
			['a', '日',],
			['b', '月',],
			['c', '金',],
			['d', '木',],
			['e', '水',],
			['f', '火',],
			['g', '土',],
			['h', '竹',],
			['i', '戈',],
			['j', '十',],
			['k', '大',],
			['l', '中',],
			['m', '一',],
			['n', '弓',],
			['o', '人',],
			['p', '心',],
			['q', '手',],
			['r', '口',],
			['s', '尸',],
			['t', '廿',],
			['u', '山',],
			['v', '女',],
			['w', '田',],
			['x', '難',],
			['y', '卜',],
			['z', '符',],
			]
		self.nameDict={
				'cn':'仓颉',
				'tw':'倉頡',
				'hk':'倉頡',
				'en':'CangJie',
				}
		self.iconfile="qhcj.svg"
		self.maxkeylength=5

class CJLump:
	def __init__(self, frontCode, containerCode, interiorCode):
		self.frontCode=frontCode
		self.containerCode=containerCode
		self.interiorCode=interiorCode

		self.isBodyContainer=False
		self.isDirtySingleton=False
	def __str__(self):
		return "%s"%self.getXCode()

	def getFrontCode(self):
		return self.frontCode

	def getContainerCode(self):
		return self.containerCode

	def getInteriorCode(self):
		return self.interiorCode

	def getXCode(self):
		return [self.frontCode, self.containerCode, self.interiorCode]

	def getHelper(self):
		return CJCodeHelper(self)

	def getCode(self, headCount, tailCount):
		helper=self.getHelper()
		return helper.getCode(headCount, tailCount).lower()

	def getCodeAsSingleton(self):
		return self.getCode(3, 1)

	def isHeadWithOne(self):
		return (len(self.getCodeAsHead())==1)

	def getCodeAsHead(self):
		return self.getCode(1, 1)

	def getCodeAsBody(self):
		return self.getCode(2, 1)

	def getCodeAsTail(self):
		return self.getCode(0, 1)

	@staticmethod
	def computeTotalCode(cjLumpList):
		code=''
		if len(cjLumpList) == 1:
			code=cjLumpList[0].getCodeAsSingleton()
		elif len(cjLumpList) > 1:
			code=cjLumpList[0].getCodeAsHead()
			code+=CJLump.computeBodyCode(cjLumpList[1:])
		else:
			code=''
		return code

	@staticmethod
	def computeBodyCode(cjLumpList):
		code=''
		if len(cjLumpList) == 1:
			cjLumpList[0].isBodyContainer=False
			code=cjLumpList[0].getCodeAsBody()
		elif len(cjLumpList) > 1:
			code=cjLumpList[0].getCodeAsHead()
			tmpCJLump=CJLump.generateBody(cjLumpList[1:])
			if(cjLumpList[0].isHeadWithOne()):
				tmpCJLump=CJLump.generateBody(cjLumpList[1:])
				code+=tmpCJLump.getCodeAsHead()
			else:
				code+=cjLumpList[-1].getCodeAsTail()
		else:
			code=''
		return code

	@staticmethod
	def computeSingletonCode(cjLumpList):
		tmpLump=CJLump.generateSingleton(cjLumpList)
		return tmpLump.getCodeAsSingleton()

	@staticmethod
	def generate(frontCode, containerCode, interiorCode):
		return CJLump(frontCode, containerCode, interiorCode)

	@staticmethod
	def generateBody(cjLumpList):
		lastCJLump=cjLumpList[-1]

		lastCJLump.isBodyContainer=True
		[frontCode, containerCode, interiorCode] = lastCJLump.getXCode()
		lastCJLump.isBodyContainer=False

		tmpFrontCode=("".join(map(lambda x: x.getCodeAsHead(), cjLumpList[:-1])))

		tmpCJLump=CJLump.generate(tmpFrontCode+frontCode, containerCode, interiorCode)
		return tmpCJLump

	@staticmethod
	def generateSingleton(cjLumpList):
		lastCJLump=cjLumpList[-1]

		lastCJLump.isBodyContainer=True
		[frontCode, containerCode, interiorCode] = lastCJLump.getXCode()
		lastCJLump.isBodyContainer=False

		tmpFrontCode=("".join(map(lambda x: x.getCodeAsBody(), cjLumpList[:-1])))

		tmpCJLump=CJLump.generate(tmpFrontCode+frontCode, containerCode, interiorCode)
		return tmpCJLump

	@staticmethod
	def generateContainer(cjLumpList):
		firstCJLump=cjLumpList[0]
		[frontCode, containerCode, interiorCode] = firstCJLump.getXCode()

		tmpCJLump=CJLump.generateBody(cjLumpList[1:])
		tmpInteriorCode=tmpCJLump.getCodeAsHead()
		cjLump=CJLump.generate(frontCode, containerCode, interiorCode)
		return ContainerCJLump(cjLump, tmpCJLump)

class ContainerCJLump(CJLump):
	def __init__(self, outerLump, innerLump):
		self.outerLump=outerLump
		self.innerLump=innerLump
		self.isBodyContainer=False

	def getHelper(self):
		return ContainerCJCodeHelper(self.outerLump, self.innerLump)

	def getCodeAsBody(self):
		code=self.outerLump.getCodeAsHead()
		if len(code)==1:
			code+=self.innerLump.getCodeAsHead()
		elif len(code)==2:
			code+=self.innerLump.getCodeAsTail()
		return code

	def getXCode(self):
		[outerFront, outerContainer, outerInterior] = self.outerLump.getXCode()
		[innerFront, innerContainer, innerInterior] = self.innerLump.getXCode()
		if self.isBodyContainer:
			return [outerFront, outerContainer, self.innerLump.getCodeAsTail()]
		else:
			return [outerFront, outerContainer, self.innerLump.getCodeAsBody()]

class CJCodeHelper:
	def __init__(self, cjLump):
		[self.frontCode, self.containerCode, self.interiorCode] = cjLump.getXCode()

		self.innerHelper=None

	def getCode(self, headCount, tailCount):
		return (self.getHeadCode(headCount)+self.getTailCode(tailCount))

	def getHeadCode(self, headCount):
		head=""
		for i in range(headCount):
			head+=self.getH()
		return head

	def getTailCode(self, tailCount):
		tail=""
		for i in range(tailCount):
			tail=tail+self.getT()
		return tail

	def getH(self):
		if self.frontCode:
			c=self.frontCode[0]
			self.frontCode=self.frontCode[1:]
			return c
		elif self.containerCode:
			c=self.containerCode[0]
			self.containerCode=self.containerCode[1:]
			return c
		elif self.interiorCode:
			c=self.interiorCode[0]
			self.interiorCode=self.interiorCode[1:]
			return c
		else:
			return ""

	def getT(self):
		if self.containerCode:
			c=self.containerCode[-1]
			self.containerCode=self.containerCode[:-1]
			return c
		elif self.interiorCode:
			c=self.interiorCode[-1]
			self.interiorCode=self.interiorCode[:-1]
			return c
		elif self.frontCode:
			c=self.frontCode[-1]
			self.frontCode=self.frontCode[:-1]
			return c
		else:
			return ""

class ContainerCJCodeHelper(CJCodeHelper):
	def __init__(self, outerLump, innerLump):
		[self.outerFrontCode, self.outerContainerCode, self.outerInteriorCode] = outerLump.getXCode()
		[self.innerFrontCode, self.innerContainerCode, self.innerInteriorCode] = innerLump.getXCode()

	def getH(self):
		if self.outerFrontCode:
			c=self.outerFrontCode[0]
			self.outerFrontCode=self.outerFrontCode[1:]
			return c
		elif self.outerContainerCode:
			c=self.outerContainerCode[0]
			self.outerContainerCode=self.outerContainerCode[1:]
			return c
		elif self.innerFrontCode:
			c=self.innerFrontCode[0]
			self.innerFrontCode=self.innerFrontCode[1:]
			return c
		elif self.innerContainerCode:
			c=self.innerContainerCode[0]
			self.innerContainerCode=self.innerContainerCode[1:]
			return c
		elif self.outerInteriorCode:
			c=self.outerInteriorCode[0]
			self.outerInteriorCode=self.outerInteriorCode[1:]
			return c
		elif self.innerInteriorCode:
			c=self.innerInteriorCode[0]
			self.innerInteriorCode=self.innerInteriorCode[1:]
			return c
		else:
			return ""

	def getT(self):
		if self.outerContainerCode:
			c=self.outerContainerCode[-1]
			self.outerContainerCode=self.outerContainerCode[:-1]
			return c
		elif self.outerInteriorCode:
			c=self.outerInteriorCode[-1]
			self.outerInteriorCode=self.outerInteriorCode[:-1]
			return c
		elif self.innerContainerCode:
			c=self.innerContainerCode[-1]
			self.innerContainerCode=self.innerContainerCode[:-1]
			return c
		elif self.innerInteriorCode:
			c=self.innerInteriorCode[-1]
			self.innerInteriorCode=self.innerInteriorCode[:-1]
			return c
		elif self.innerFrontCode:
			c=self.innerFrontCode[-1]
			self.innerFrontCode=self.innerFrontCode[:-1]
			return c
		elif self.outerFrontCode:
			c=self.outerFrontCode[-1]
			self.outerFrontCode=self.outerFrontCode[:-1]
			return c
		else:
			return ""

class CJCodeInfo(CodeInfo):
	def __init__(self, direction, cjLumpList, cjLumpListSingleton):
		super().__init__()

		self.direction=direction
		self.cjLumpList=cjLumpList
		self.cjLumpListSingleton=cjLumpListSingleton

	@staticmethod
	def generateDefaultCodeInfo(direction, cjLumpList):
		codeInfo=CJCodeInfo(direction, cjLumpList, None)

		return codeInfo

	def toCode(self):
		direction=self.getDirection()

		if self.cjLumpListSingleton:
			rtlist=self.cjLumpList
			rtlist=self.cjLumpListSingleton
			return CJLump.computeTotalCode(rtlist)
		else:
			rtlist=self.cjLumpList
			if direction=='$':
				return CJLump.computeSingletonCode(rtlist)
			else:
				return CJLump.computeTotalCode(rtlist)


	def getDirection(self):
		return self.direction

	def getLumpList(self):
		return self.cjLumpList

class GridCJCodeInfo(CJCodeInfo):
	def __init__(self, codeInfoV, codeInfoH):
		CodeInfo.__init__(self)
#		super().__init__(codeInfoV.getDirection, codeInfoV.getLumpList, None)
		self.codeInfoV=codeInfoV
		self.codeInfoH=codeInfoH

	def toCode(self):
		return self.codeInfoV.toCode()

	def getDirection(self):
		return '+'

	def getLumpList(self):
		return self.codeInfoV.getLumpList()

	def getCodeInfoH(self):
		return self.codeInfoH

	def getCodeInfoV(self):
		return self.codeInfoV

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

class CJRadixParser(CodingRadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_SINGLETON_EXPRESSION='獨體表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		description=infoDict.get(CJRadixParser.ATTRIB_CODE_EXPRESSION)
		direction=description[0]

		description_singleton=infoDict.get(CJRadixParser.ATTRIB_SINGLETON_EXPRESSION)

		cjLumpList=self.parseCJLumpList(description[1:])
		cjLumpList_singleton=self.parseCJLumpList(description_singleton)
		codeInfo=CJCodeInfo(direction, cjLumpList, cjLumpList_singleton)

		return codeInfo

	def parseCJLumpList(self, description):
		cjLumpList=[]

		if description!=None:
			description_list=description.split(",")
			for desc in description_list:
				matchResult=re.match("(\w*)(\[(\w*)\](\w*))?", desc)
				groups=matchResult.groups()
				frontCode=groups[0]
				tailingSurround=groups[2]
				rearCode=groups[3]
				if tailingSurround==None:
					tailingSurround=""

				matchResult=re.match("([A-Z]*)([a-z]*)", tailingSurround)
				groups=matchResult.groups()

				containerCode=groups[0]
				interiorCode=groups[1]

				cjLump=CJLump.generate(frontCode, containerCode, interiorCode)
				cjLumpList.append(cjLump)

		return cjLumpList

