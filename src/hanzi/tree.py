import abc
from injector import inject


from element.operator import Operator

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


TreeNodeType = object


class TreeNodeGenerator(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generateLeafNode(self, reference: (str, int)) -> TreeNodeType:
        pass

    @abc.abstractmethod
    def generateNode(
        self, operator: Operator, children: tuple[TreeNodeType]
    ) -> TreeNodeType:
        pass

    @abc.abstractmethod
    def generateLeafNodeByReference(
        self, node: TreeNodeType, index: int
    ) -> TreeNodeType:
        pass
