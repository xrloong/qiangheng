from injector import inject

from workspace import HanZiWorkspaceManager
from model.helper import OperatorManager

from tree.regexp.item import TreeRegExp
from tree.regexp import TreeRegExpInterpreter
from tree.regexp import BasicTreeProxy
from tree.regexp import TreeNodeGenerator


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
    def __init__(
        self, treeProxy: HanZiTreeProxy, treeNodeGenerator: HanZiTreeNodeGenerator
    ):
        super().__init__(HanZiTreeProxy())
        self.treeNodeGenerator = treeNodeGenerator

    def replace(self, tre: TreeRegExp, result: str):
        def generateTokens(expression):
            tokens = []
            length = len(expression)
            i = 0
            while i < length:
                if expression[i] in ["(", ")"]:
                    tokens.append(expression[i])
                    i += 1
                elif expression[i] == "\\":
                    j = i + 1
                    while (
                        j < length and expression[j].isdigit() or expression[j] == "."
                    ):
                        j += 1
                    tokens.append(expression[i:j])
                    i = j
                elif expression[i] == " ":
                    i += 1
                else:
                    j = i + 1
                    while j < length and expression[j] not in ["(", ")", "\\", " "]:
                        j += 1
                    tokens.append(expression[i:j])
                    i = j
            return tokens

        def genStructDesc(expression, allComps):
            return genStructDescRecursive(generateTokens(expression), allComps)[1]

        def genStructDescRecursive(tokens, allComps):
            if not tokens[0] == "(":
                return ([], None)

            treeNodeGenerator = self.treeNodeGenerator
            operatorName = tokens[1]
            compList = []
            rest = tokens[2:]
            while len(rest) > 0:
                if rest[0] == "(":
                    rest, structDesc = genStructDescRecursive(rest, allComps)
                    if structDesc is not None:
                        compList.append(structDesc)
                elif rest[0] == ")":
                    rest = rest[1:]
                    break
                elif rest[0][:1] == "\\":
                    refExp = rest[0][1:]
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
                        node = treeNodeGenerator.generateLeafNodeByReference(
                            referenceNode, subIndex
                        )
                        compList.append(node)
                    rest = rest[1:]
                else:
                    compList.append(treeNodeGenerator.generateLeafNode(rest[0]))
                    rest = rest[1:]
            structDesc = treeNodeGenerator.generateNode(operatorName, compList)
            return (rest, structDesc)

        return genStructDesc(result, tre.getAll())
