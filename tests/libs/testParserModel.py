import unittest

from pydantic import ValidationError

from element.enum import CodeVariance
from element.enum import FontVariance
from parser.model import CharacterDecompositionSetModel
from parser.model import RadixCodeInfoModel
from parser.model import RadicalSetModel
from parser.model import StructureModel
from parser.model import SubstituteRuleMatchingModel
from parser.model import SubstituteRuleModel


class RadixCodeInfoModelTestCase(unittest.TestCase):
    def testDefaultVarianceIsStandard(self):
        model = RadixCodeInfoModel()
        self.assertEqual(model.variance, CodeVariance.STANDARD)

    def testTolerantVariance(self):
        model = RadixCodeInfoModel(類型="容錯")
        self.assertEqual(model.variance, CodeVariance.TOLERANT)

    def testSimplifiedVarianceIsRejected(self):
        with self.assertRaises(ValidationError):
            RadixCodeInfoModel(類型="簡快")

    def testSupportCharacterCode(self):
        model = RadixCodeInfoModel(字符碼="是")
        self.assertFalse(model.isSupportRadixCode)

    def testSupportRadixCodeByDefault(self):
        model = RadixCodeInfoModel()
        self.assertTrue(model.isSupportRadixCode)

    def testSupportCharacterCodeOnlyAccepts是(self):
        with self.assertRaises(ValidationError):
            RadixCodeInfoModel(字符碼="否")

    def testExtraFieldsAreAllowed(self):
        model = RadixCodeInfoModel(編碼表示式="*m")
        self.assertEqual(model.編碼表示式, "*m")


class StructureModelTestCase(unittest.TestCase):
    def testDefaultFontIsAll(self):
        model = StructureModel(結構="()")
        self.assertEqual(model.expression, "()")
        self.assertEqual(model.font, FontVariance.All)

    def testTraditionalFont(self):
        model = StructureModel(結構="({運算=爲}({置換=倉}))", 字體="傳")
        self.assertEqual(model.font, FontVariance.Traditional)

    def testSimplifiedFont(self):
        model = StructureModel(結構="({運算=爲}({置換=仓}))", 字體="簡")
        self.assertEqual(model.font, FontVariance.Simplified)

    def testExplicitAllFontIsRejected(self):
        with self.assertRaises(ValidationError):
            StructureModel(結構="()", 字體="全")


class SubstituteRuleModelTestCase(unittest.TestCase):
    def testMatchingAsPattern(self):
        model = SubstituteRuleModel(
            比對="({運算=同} ({名稱=戌}) .)", 替換="(同 戊 (蚕 一 \\2))"
        )
        self.assertEqual(model.matching, "({運算=同} ({名稱=戌}) .)")
        self.assertEqual(model.replacement, "(同 戊 (蚕 一 \\2))")

    def testMatchingAsOperatorAndOperandCount(self):
        model = SubstituteRuleModel(
            比對=SubstituteRuleMatchingModel(運算="蚕", 參數個數=3),
            替換="(蚕 \\1 \\2 \\3)",
        )
        self.assertIsInstance(model.matching, SubstituteRuleMatchingModel)
        self.assertEqual(model.matching.operator, "蚕")
        self.assertEqual(model.matching.operandCount, 3)

    def testTemplateFieldsDefaultToNone(self):
        model = SubstituteRuleModel(比對="({名稱=一})", 替換="(乙)")
        self.assertIsNone(model.templateName)
        self.assertIsNone(model.parameterCount)


class RadicalSetModelTestCase(unittest.TestCase):
    def testLoadRadicalSet(self):
        model = RadicalSetModel(
            字符集=[
                {
                    "名稱": "一",
                    "註記": "U+4E00",
                    "編碼資訊": [{"編碼表示式": "*m"}],
                }
            ]
        )

        self.assertEqual(len(model.radicals), 1)
        radical = model.radicals[0]
        self.assertEqual(radical.name, "一")
        self.assertEqual(radical.comment, "U+4E00")
        self.assertEqual(len(radical.codings), 1)


class CharacterDecompositionSetModelTestCase(unittest.TestCase):
    def testLoadDecompositionSet(self):
        model = CharacterDecompositionSetModel(
            字符集=[
                {
                    "名稱": "瑲",
                    "註記": "U+7472",
                    "結構集": [{"結構": "({運算=鴻}({置換=王})({置換=倉}))"}],
                }
            ]
        )

        self.assertEqual(len(model.decompositionSet), 1)
        decomposition = model.decompositionSet[0]
        self.assertEqual(decomposition.name, "瑲")
        self.assertEqual(
            decomposition.structureSet[0].expression,
            "({運算=鴻}({置換=王})({置換=倉}))",
        )


if __name__ == "__main__":
    unittest.main()
