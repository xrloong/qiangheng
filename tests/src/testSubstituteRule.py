import unittest

from model.element.SubstituteRule import SubstituteRule
from model.element.SubstituteRule import SubstituteRuleSet
from parser.model import SubstituteRuleMatchingModel
from parser.model import SubstituteRuleModel
from parser.model import SubstituteRuleSetModel
from tree.node import Node


class SubstituteRuleTestCase(unittest.TestCase):
    def testRuleFromPatternString(self):
        model = SubstituteRuleModel(
            比對="({運算=同} ({名稱=戌}) .)", 替換="(同 戊 (蚕 一 \\2))"
        )
        rule = SubstituteRule(model)

        tre = rule.tre
        self.assertEqual(tre.prop, {"運算": "同"})
        self.assertEqual(len(tre.children), 2)
        self.assertEqual(tre.children[0].prop, {"名稱": "戌"})
        self.assertTrue(tre.children[1].isDot())

    def testGoalTreeWithBackReference(self):
        model = SubstituteRuleModel(
            比對="({運算=同} ({名稱=戌}) .)", 替換="(同 戊 (蚕 一 \\2))"
        )
        rule = SubstituteRule(model)

        goalAnswer = Node(
            prop={"運算": "同"},
            children=(
                Node(prop={"置換": "戊"}),
                Node(
                    prop={"運算": "蚕"},
                    children=(
                        Node(prop={"置換": "一"}),
                        Node(backRefExp="\\2"),
                    ),
                ),
            ),
        )
        self.assertEqual(rule.goal, goalAnswer)

    def testRuleFromOperatorAndOperandCount(self):
        # 以「運算＋參數個數」比對時，展開為各參數皆為 . 的樣式
        model = SubstituteRuleModel(
            比對=SubstituteRuleMatchingModel(運算="蚕", 參數個數=3),
            替換="(蚕 \\1 \\2 \\3)",
        )
        rule = SubstituteRule(model)

        tre = rule.tre
        self.assertEqual(tre.prop, {"運算": "蚕"})
        self.assertEqual(len(tre.children), 3)
        for child in tre.children:
            self.assertTrue(child.isDot())


class SubstituteRuleSetTestCase(unittest.TestCase):
    def testBuildRules(self):
        model = SubstituteRuleSetModel(
            規則集=[
                {"比對": "({名稱=一})", "替換": "(乙)"},
                {"比對": "({運算=同} ({名稱=戌}) .)", "替換": "(同 戊 (蚕 一 \\2))"},
            ]
        )
        ruleSet = SubstituteRuleSet(model)

        self.assertEqual(len(ruleSet.rules), 2)
        self.assertEqual(ruleSet.rules[0].tre.prop, {"名稱": "一"})
        self.assertEqual(ruleSet.rules[1].tre.prop, {"運算": "同"})


if __name__ == "__main__":
    unittest.main()
