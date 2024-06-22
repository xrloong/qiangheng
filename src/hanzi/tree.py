from injector import inject

from workspace import HanZiWorkspaceManager
from model.helper import OperatorManager

from tree.regexp import BasicTreeProxy


class HanZiTreeProxy(BasicTreeProxy):
    @inject
    def __init__(self):
        pass

    def getChildren(self, currentStructure):
        return currentStructure.getExpandedStructureList()

    def matchSingle(self, tre, currentStructure):
        prop = tre.prop
        opName = prop.get("運算")
        refExp = prop.get("名稱")
        return currentStructure.isMatchStructure(
            operatorName=opName, referenceExpression=refExp
        )


class TreeNodeGenerator:
    def generateLeafNode(self, nodeName):
        return None

    def generateNode(self, operatorName, children):
        return None

    def generateLeafNodeByReference(self, referencedNode, index):
        return None


class HanZiTreeNodeGenerator(TreeNodeGenerator):
    @inject
    def __init__(
        self,
        workspaceManager: HanZiWorkspaceManager,
        operatorManager: OperatorManager,
    ):
        self.__workspaceManager = workspaceManager
        self.__operatorManager = operatorManager

    def generateLeafNode(self, nodeName):
        return self.__workspaceManager.getWrapperStructure(nodeName)

    def generateLeafNodeByReference(self, referencedTreeNode, index):
        return self.__workspaceManager.getWrapperStructure(
            referencedTreeNode.referencedNodeName, index
        )

    def generateNode(self, operatorName, children):
        operator = self.__operatorManager.generateOperator(operatorName)
        return self.__workspaceManager.generateCompoundStructure(operator, children)
