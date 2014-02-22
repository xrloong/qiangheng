import re
import sys

class CJLump:
	def __init__(self, frontCode, containerCode, interiorCode):
		self.frontCode=frontCode
		self.containerCode=containerCode
		self.interiorCode=interiorCode

		self.isBodyContainer=False
		self.isDirtySingleton=False
	def __str__(self):
#		return "(%s,%s,%s)"%self.getXCode()
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

	def getCodeAsHeadHead(self):
		return self.getCode(1, 0)

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

