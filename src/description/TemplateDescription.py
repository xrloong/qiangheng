#!/usr/bin/env python3

import sys
import copy

class TemplateSubstitutionDescription:
	"""樣本結構描述"""
	def __init__(self, structure):
		self.structure=structure

	def getStructure(self):
		return self.structure

	def isMatch(self, parameterToArgumentNameMapping):
		return True

class TemplateDescription:
	"""樣本描述"""
	countAnonymousName=0
	def __init__(self, name, parameterList, substitutionList):
		self.name=name

		self.substitutionList=substitutionList
		self.parameterList=parameterList

	def __str__(self):
		return '{0}({2})={1}'.format(self.name, self.charDesc, self.parameterList)

	def __repr__(self):
		return str(self)

	def getName(self):
		return self.name

	def setParameterList(self, parameterList):
		self.parameterList=parameterList

	def rearrange(self, charDesc):
		def getMapping(parameterList, argumentList):
			parameterToArgumentMapping={}
			parameterToArgumentNameMapping={}
			if len(argumentList)==len(parameterList):
				argumentNameList=map(lambda x: x.getReferenceName(), argumentList)
				pairList=zip(parameterList, argumentList)
				namePairList=zip(parameterList, argumentNameList)

				parameterToArgumentMapping=dict(pairList)
				parameterToArgumentNameMapping=dict(namePairList)
			else:
				print("參數列及引數列個數不符", file=sys.stderr)
			return (parameterToArgumentMapping, parameterToArgumentNameMapping)

		# 需要先替換兒子，才可以進行自己的替換。
		# 否則，如：條=(範翛 木)=(範湘 亻丨(志 夂木))
		# 而 '木' 會被誤判為湘的參數。
		def replaceCharDesc(charDesc):
			for comp in charDesc.getCompList():
				replaceCharDesc(comp)

#			argumentDesc=parameterToArgumentMapping.get(charDesc.getReferenceName())
			argumentDesc=getWantedReplaceDescription(charDesc)
			if argumentDesc!=None:
				charDesc.replacedBy(argumentDesc)

		def getWantedReplaceDescription(charDesc):
			referenceName=charDesc.getReferenceName()
			targetArgumentDesc=parameterToArgumentMapping.get(referenceName)
			referenceExpression=charDesc.getReferenceExpression()

#			argumentDesc=copy.deepcopy(targetArgumentDesc)
			argumentDesc=None
			if targetArgumentDesc:
				argumentDesc=targetArgumentDesc.copyDeeply()
				argumentReferenceName=argumentDesc.getReferenceName()
				argumentReferenceExpression=argumentDesc.getReferenceName()
				if referenceExpression and argumentReferenceExpression and referenceExpression.count(".")>0 and argumentReferenceExpression.count(".")==0:
					expList=referenceExpression.split(".")
					expList[0]=argumentReferenceName
					newExpression=".".join(expList)
					argumentDesc.setReferenceExpression(newExpression)
				elif referenceExpression and argumentReferenceExpression and referenceExpression.count(".")==0 and argumentReferenceExpression.count(".")>0:
					pass
				return argumentDesc

		def getMatchedStructureDescription(parameterToArgumentNameMapping):
			targetCharDesc=None
			for substitution in self.substitutionList:
				if substitution.isMatch(parameterToArgumentNameMapping):
					targetCharDesc=substitution.getStructure()
					break
			else:
				print("沒考到符合條件的結構", file=sys.stderr)

			tempDesc=targetCharDesc.copyDeeply()
			return tempDesc

		argumentList=charDesc.getCompList()
		parameterList=self.parameterList
		mappings=getMapping(parameterList, argumentList)
		(parameterToArgumentMapping, parameterToArgumentNameMapping)=mappings

		targetStructureDescription=getMatchedStructureDescription(parameterToArgumentNameMapping)
		replaceCharDesc(targetStructureDescription)
		charDesc.replacedBy(targetStructureDescription)


if __name__=='__main__':
	print(TemplateDescription('王', '(龜)', None))

