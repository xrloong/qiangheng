import unittest

from tree.regexp import compile
from tree.regexp import TreeRegExpInterpreter
from tree.regexp import BasicTreeProxy


def leaf(name):
    return {"name": name}


def node(operator, *children):
    return {"operator": operator, "children": list(children)}


class TreeRegExpParserTestCase(unittest.TestCase):
    def testParseLeafPattern(self):
        tre = compile("({名稱=戌})")

        self.assertEqual(tre.prop, {"名稱": "戌"})
        self.assertEqual(tre.children, [])

    def testParseEmptyProp(self):
        tre = compile("({})")

        self.assertEqual(tre.prop, {})
        self.assertEqual(tre.children, [])

    def testParseDotChildren(self):
        tre = compile("({運算=蚕} . .)")

        self.assertEqual(tre.prop, {"運算": "蚕"})
        self.assertEqual(len(tre.children), 2)
        self.assertTrue(tre.children[0].isDot())
        self.assertTrue(tre.children[1].isDot())
        self.assertFalse(tre.children[0].isWithStar())

    def testParseStar(self):
        tre = compile("({運算=同} ({名稱=戌}) .*)")

        self.assertEqual(len(tre.children), 2)
        self.assertFalse(tre.children[0].isWithStar())
        self.assertTrue(tre.children[1].isDot())
        self.assertTrue(tre.children[1].isWithStar())

    def testParseNestedPattern(self):
        tre = compile("({運算=廖} ({名稱=厂}) ({運算=蚕} ({名稱=一}) .*))")

        self.assertEqual(tre.prop, {"運算": "廖"})
        self.assertEqual(len(tre.children), 2)

        first, second = tre.children
        self.assertEqual(first.prop, {"名稱": "厂"})
        self.assertEqual(second.prop, {"運算": "蚕"})
        self.assertEqual(second.children[0].prop, {"名稱": "一"})
        self.assertTrue(second.children[1].isWithStar())

    def testGetCompTraversesInPrefixOrder(self):
        tre = compile("({運算=廖} ({名稱=厂}) ({運算=蚕} ({名稱=一}) .))")

        self.assertEqual(tre.getComp(0), tre)
        self.assertEqual(tre.getComp(1), tre.children[0])
        self.assertEqual(tre.getComp(2), tre.children[1])
        self.assertEqual(tre.getComp(3), tre.children[1].children[0])
        self.assertEqual(tre.getComp(4), tre.children[1].children[1])
        self.assertIsNone(tre.getComp(5))


class TreeRegExpInterpreterTestCase(unittest.TestCase):
    def setUp(self):
        self.interpreter = TreeRegExpInterpreter(BasicTreeProxy())

    def testMatchLeafByName(self):
        tre = compile("({名稱=戌})")

        self.assertTrue(self.interpreter.match(tre, leaf("戌")).isMatched())
        self.assertFalse(self.interpreter.match(tre, leaf("戊")).isMatched())

    def testMatchByOperator(self):
        tre = compile("({運算=蚕} . .)")

        self.assertTrue(
            self.interpreter.match(tre, node("蚕", leaf("上"), leaf("下"))).isMatched()
        )
        self.assertFalse(
            self.interpreter.match(tre, node("鴻", leaf("王"), leaf("倉"))).isMatched()
        )

    def testMatchRequiresExactChildCount(self):
        tre = compile("({運算=蚕} . .)")

        self.assertFalse(self.interpreter.match(tre, node("蚕", leaf("一"))).isMatched())
        self.assertFalse(
            self.interpreter.match(
                tre, node("蚕", leaf("一"), leaf("二"), leaf("三"))
            ).isMatched()
        )

    def testMatchNamedChildren(self):
        tre = compile("({運算=蚕} ({名稱=上}) ({名稱=下}))")

        self.assertTrue(
            self.interpreter.match(tre, node("蚕", leaf("上"), leaf("下"))).isMatched()
        )
        self.assertFalse(
            self.interpreter.match(tre, node("蚕", leaf("下"), leaf("上"))).isMatched()
        )

    def testMatchNestedPattern(self):
        tre = compile("({運算=廖} ({名稱=厂}) ({運算=蚕} ({名稱=一}) .))")
        tree = node("廖", leaf("厂"), node("蚕", leaf("一"), leaf("从")))

        self.assertTrue(self.interpreter.match(tre, tree).isMatched())

    def testStarMatchesZeroNodes(self):
        tre = compile("({運算=同} ({名稱=戌}) .*)")

        self.assertTrue(self.interpreter.match(tre, node("同", leaf("戌"))).isMatched())

    def testStarMatchesManyNodes(self):
        tre = compile("({運算=同} ({名稱=戌}) .*)")
        tree = node("同", leaf("戌"), leaf("一"), leaf("口"))

        self.assertTrue(self.interpreter.match(tre, tree).isMatched())

    def testStarCapturesMatchedNodes(self):
        tre = compile("({運算=同} ({名稱=戌}) .*)")
        node一 = leaf("一")
        node口 = leaf("口")
        tree = node("同", leaf("戌"), node一, node口)

        self.assertTrue(self.interpreter.match(tre, tree).isMatched())

        starTre = tre.children[1]
        self.assertEqual(starTre.getMatched(), [node一, node口])

    def testMatchedNodesAreRecorded(self):
        tre = compile("({運算=蚕} ({名稱=上}) ({名稱=下}))")
        node上 = leaf("上")
        node下 = leaf("下")
        tree = node("蚕", node上, node下)

        self.assertTrue(self.interpreter.match(tre, tree).isMatched())
        self.assertEqual(tre.getMatched(), [tree])
        self.assertEqual(tre.children[0].getMatched(), [node上])
        self.assertEqual(tre.children[1].getMatched(), [node下])


if __name__ == "__main__":
    unittest.main()
