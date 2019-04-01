from injector import inject

import model
from model.element.StructureDescription import StructureDescription

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: model.OperatorManager.OperatorManager):
		self.operationManager = operationManager

	def generateLeafNode(self, nodeExpression):
		structDesc=self.generateNode()
		structDesc.setReferenceExpression(nodeExpression)
		structDesc.generateName()
		return structDesc

	def generateNode(self, structInfo=['龜', []]):
		operatorName, compList=structInfo
		operator=self.operationManager.generateOperator(operatorName)
		structDesc=StructureDescription(operator, compList)
		structDesc.generateName()
		return structDesc


