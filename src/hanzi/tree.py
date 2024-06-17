from injector import inject

from workspace import HanZiWorkspaceManager
from model.helper import OperatorManager

from tree.regexp.item import TreeRegExp
from tree.regexp import TreeRegExpInterpreter
from tree.regexp import BasicTreeProxy
from tree.regexp import TreeNodeGenerator

from tree.node import Node as TreeExpression
from tree.parser import TreeParser


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


class HanZiTreeRegExpInterpreter(TreeRegExpInterpreter):
    @inject
    def __init__(self, treeNodeGenerator: HanZiTreeNodeGenerator):
        super().__init__(HanZiTreeProxy())
        self.treeNodeGenerator = treeNodeGenerator

    def replace(self, tre: TreeRegExp, goalNode: TreeExpression):
        treeNodeGenerator = self.treeNodeGenerator

        def convertNodeToStructure(node: TreeExpression, allComps):
            operatorName = node.prop["運算"]
            compList = []
            for childNode in node.children:
                if "置換" in childNode.prop:
                    compList.append(
                        treeNodeGenerator.generateLeafNode(childNode.prop["置換"])
                    )
                elif childNode.isBackRef:
                    # \1 or \1.1
                    refExp = childNode.backRefExp

                    refExp = refExp[1:]
                    refExpList = refExp.split(".")
                    if len(refExpList) < 2:
                        # \1
                        index = int(refExpList[0])
                        compList.extend(allComps[index].getMatched())
                    else:
                        # \1.1
                        index = int(refExpList[0])
                        subIndex = int(refExpList[1])
                        referenceNode = allComps[index].getMatched()[0]
                        comp = treeNodeGenerator.generateLeafNodeByReference(
                            referenceNode, subIndex
                        )
                        compList.append(comp)
                else:
                    comp = convertNodeToStructure(childNode, allComps)
                    compList.append(comp)
            structDesc = treeNodeGenerator.generateNode(operatorName, compList)
            return structDesc

        return convertNodeToStructure(goalNode, tre.getAll())
