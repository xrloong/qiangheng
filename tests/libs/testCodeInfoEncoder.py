import unittest
from types import SimpleNamespace

from coding.Base import CodeInfoEncoder
from coding.Base.Base import CodeInfo
from element.enum import CodeVariance
from element.operator import Operator


def fake(code):
    return SimpleNamespace(code=code)


class ConcatCodeInfoEncoder(CodeInfoEncoder):
    """只實作龍運算（串接編碼），其餘運算皆退回預設實作。"""

    def encodeAsLoong(self, codeInfoList):
        return fake("".join(codeInfo.code for codeInfo in codeInfoList))


class UnavailableCodeInfoEncoder(ConcatCodeInfoEncoder):
    def isAvailableOperation(self, codeInfoList):
        return False


class CodeInfoTestCase(unittest.TestCase):
    def testDefaultAttributes(self):
        codeInfo = CodeInfo()

        self.assertEqual(codeInfo.getCodeVariance(), CodeVariance.STANDARD)
        self.assertTrue(codeInfo.isSupportRadixCode())

    def testMultiplyCodeVariance(self):
        codeInfo = CodeInfo()
        codeInfo.multiplyCodeVariance(CodeVariance.TOLERANT)

        self.assertEqual(codeInfo.getCodeVariance(), CodeVariance.TOLERANT)

        codeInfo.multiplyCodeVariance(CodeVariance.STANDARD)
        self.assertEqual(codeInfo.getCodeVariance(), CodeVariance.TOLERANT)

    def testSetCodeInfoAttribute(self):
        codeInfo = CodeInfo()
        codeInfo.setCodeInfoAttribute(
            codeVariance=CodeVariance.SIMPLIFIED, isSupportRadixCode=False
        )

        self.assertEqual(codeInfo.getCodeVariance(), CodeVariance.SIMPLIFIED)
        self.assertFalse(codeInfo.isSupportRadixCode())


class CodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = ConcatCodeInfoEncoder()

    def encode(self, operator, codes):
        codeInfo = self.encoder.setByComps(operator, [fake(code) for code in codes])
        return codeInfo.code

    def testLoong(self):
        self.assertEqual(self.encode(Operator.Loong, ["王", "倉"]), "王倉")

    def testDefaultOperatorsFallBackToLoong(self):
        for operator in (
            Operator.Silkworm,
            Operator.Goose,
            Operator.Loop,
            Operator.Qi,
            Operator.Zhe,
            Operator.Liao,
            Operator.Zai,
            Operator.Dou,
            Operator.Tong,
            Operator.Qu,
            Operator.Han,
            Operator.Left,
            Operator.Mu,
            Operator.You,
            Operator.Liang,
            Operator.Jia,
        ):
            with self.subTest(operator=str(operator)):
                self.assertEqual(self.encode(operator, ["王", "倉"]), "王倉")

    def testEqualDelegatesToLoong(self):
        self.assertEqual(self.encode(Operator.Equal, ["倉"]), "倉")

    def testZuoReordersOperands(self):
        # 㘴的參數順序為土、口、人，編碼時轉為口、人、土
        self.assertEqual(self.encode(Operator.Zuo, ["土", "口", "人"]), "口人土")

    def testLuanRepeatsSecondOperand(self):
        # 䜌：言在中，糸在兩側
        self.assertEqual(self.encode(Operator.Luan, ["言", "糸"]), "糸言糸")

    def testBanRepeatsFirstOperand(self):
        # 辦：力在中，辛在兩側
        self.assertEqual(self.encode(Operator.Ban, ["辛", "力"]), "辛力辛")

    def testLin(self):
        self.assertEqual(self.encode(Operator.Lin, ["米", "夕", "舛"]), "米夕舛")

    def testLi(self):
        self.assertEqual(
            self.encode(Operator.Li, ["虫", "虫", "虫", "皿"]), "虫虫虫皿"
        )

    def testYiRepeatsSingleOperandFourTimes(self):
        self.assertEqual(self.encode(Operator.Yi, ["火"]), "火火火火")

    def testUnimplementedOperatorRaises(self):
        with self.assertRaises(NotImplementedError):
            self.encode(Operator.Turtle, ["王", "倉"])

    def testUnknownOperatorRaises(self):
        with self.assertRaises(NotImplementedError):
            self.encode(Operator("未知"), ["王", "倉"])

    def testUnavailableOperationReturnsNone(self):
        encoder = UnavailableCodeInfoEncoder()
        codeInfo = encoder.setByComps(Operator.Loong, [fake("王"), fake("倉")])

        self.assertIsNone(codeInfo)

    def testGenerateDefaultCodeInfo(self):
        codeInfo = self.encoder.generateDefaultCodeInfo()

        self.assertIsInstance(codeInfo, CodeInfo)
        self.assertEqual(codeInfo.code, "")


if __name__ == "__main__":
    unittest.main()
