from .item import TreeRegExp
from .item import MatchResult
from .item import BasicTreeProxy


class TreeRegExpInterpreter:
    def __init__(self, proxy: BasicTreeProxy):
        self.proxy = proxy

    def match(self, tre: TreeRegExp, node):
        return self.matchTree(tre, node)

    def matchTree(self, tre: TreeRegExp, node):
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

    def matchNode(self, tre: TreeRegExp, node):
        return self.proxy.matchSingle(tre, node)

    def matchChildren(self, tre: TreeRegExp, node):
        re_list = tre.children
        node_list = self.proxy.getChildren(node)

        if len(re_list) == 0:
            result = MatchResult()
            result.setTrue()
            return result

        return self.matchList(re_list, node_list)

    def matchList(self, treList: list[TreeRegExp], nodeList: list):
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

    def matchStar(
        self, treList: list[TreeRegExp], nodeList: list, targetTre: TreeRegExp
    ):
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
