from .item import TreeRegExp
from .item import MatchResult
from .item import BasicTreeProxy


class TreeRegExpInterpreter:
    def __init__(self, proxy: BasicTreeProxy):
        self.proxy = proxy

    def match(self, tre: TreeRegExp, node) -> MatchResult:
        result = MatchResult()
        if self.matchTree(tre, node):
            result.setTrue()
        else:
            result.setFalse()
        return result

    def matchTree(self, tre: TreeRegExp, node) -> bool:
        if self.proxy.matchSingle(tre, node) and self.matchChildren(tre, node):
            tre.setMatched([node])
            return True
        tre.setMatched([])
        return False

    def matchChildren(self, tre: TreeRegExp, node) -> bool:
        treList = tre.children
        if not treList:
            return True
        return self.matchList(treList, 0, self.proxy.getChildren(node), 0)

    def matchList(
        self, treList: list[TreeRegExp], treIndex: int, nodeList: list, nodeIndex: int
    ) -> bool:
        treCount = len(treList)
        nodeCount = len(nodeList)
        while True:
            if treIndex == treCount:
                return nodeIndex == nodeCount

            tre = treList[treIndex]
            if tre.isWithStar():
                return self.matchStar(
                    treList, treIndex + 1, nodeList, nodeIndex, tre
                )

            if nodeIndex == nodeCount:
                return False

            node = nodeList[nodeIndex]
            isMatched = self.matchTree(tre, node)
            if tre.isDot() or isMatched:
                tre.setMatched([node])
                treIndex += 1
                nodeIndex += 1
            else:
                return False

    def matchStar(
        self,
        treList: list[TreeRegExp],
        treIndex: int,
        nodeList: list,
        nodeIndex: int,
        targetTre: TreeRegExp,
    ) -> bool:
        # 保留原行為：星號樣式先走訪所有剩餘節點（不過濾，僅留下
        # setMatched 副作用），再從最長前綴往回嘗試比對其餘樣式
        for index in range(nodeIndex, len(nodeList)):
            self.matchTree(targetTre, nodeList[index])

        index = len(nodeList)
        while index >= nodeIndex:
            if self.matchList(treList, treIndex, nodeList, index):
                targetTre.setMatched(list(nodeList[nodeIndex:index]))
                return True
            index -= 1
        return False
