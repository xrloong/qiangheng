from .item import MatchResult
from .item import BasicTreeProxy
from .item import TreeNodeGenerator


class TreeRegExpInterpreter:
    def __init__(self, proxy: BasicTreeProxy, treeNodeGenerator: TreeNodeGenerator):
        self.proxy = proxy
        self.treeNodeGenerator = treeNodeGenerator

    def matchAndReplace(self, tre, node, result):
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
                    if structDesc != None:
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

        matchResult = self.match(tre, node)
        if matchResult.isMatched():
            return genStructDesc(result, tre.getAll())
        else:
            return None

    def match(self, tre, node):
        return self.matchTree(tre, node)

    def matchTree(self, tre, node):
        result = MatchResult()
        result1 = self.matchNode(tre, node)
        if result1:
            result2 = self.matchChildren(tre, node)
            if result2.isMatched():
                tre.setMatched([node])
                result.setTrue()
            else:
                tre.setMatched([])
                result.setFalse()
        else:
            tre.setMatched([])
            result.setFalse()
        return result

    def matchNode(self, tre, node):
        return self.proxy.matchSingle(tre, node)

    def matchChildren(self, tre, node):
        re_list = tre.children
        node_list = self.proxy.getChildren(node)

        if len(re_list) == 0:
            result = MatchResult()
            result.setTrue()
            return result

        return self.matchList(re_list, node_list)

    def matchList(self, treList, nodeList):
        if len(treList) == 0 and len(nodeList) == 0:
            result = MatchResult()
            result.setTrue()
            return result

        if len(treList) > 0 and treList[0].isWithStar():
            targetTre = treList[0]
            return self.matchStar(treList[1:], nodeList, targetTre)

        if len(treList) > 0 and len(nodeList) > 0:
            r = treList[0]
            n = nodeList[0]
            result = self.matchTree(r, n)
            if r.isDot() or result.isMatched():
                r.setMatched([n])
                return self.matchList(treList[1:], nodeList[1:])
        result = MatchResult()
        result.setFalse()
        return result

    def matchStar(self, treList, nodeList, targetTre):
        index = 0
        while index < len(nodeList):
            node = nodeList[index]
            if self.matchTree(targetTre, node):
                pass
            else:
                break
            index += 1

        while index >= 0:
            result = self.matchList(treList, nodeList[index:])
            if result.isMatched():
                result = MatchResult()
                targetTre.setMatched(list(nodeList[:index]))
                result.setTrue()
                return result
            index -= 1

        result = MatchResult()
        result.setFalse()
        return result
