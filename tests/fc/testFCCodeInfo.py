import unittest

from coding.FourCorner.FourCorner import FCCodeInfo
from coding.FourCorner.FourCorner import FCCodeInfoEncoder
from coding.FourCorner.constant import FCCorner
from coding.FourCorner.constant import FCStroke
from coding.FourCorner.item import FCLump
from coding.FourCorner.util import convertCornerCodeToCornerUnits
from element.operator import Operator


def lump(cornerCode, sl=False):
    return FCLump(convertCornerCodeToCornerUnits(cornerCode), sl)


def codeInfo(cornerCode, sl=False):
    return FCCodeInfo(lump(cornerCode, sl))


class FCCodeInfoTestCase(unittest.TestCase):
    def testCodeFromStrokes(self):
        self.assertEqual(codeInfo("7722").code, "7722")
        self.assertEqual(codeInfo("1234").code, "1234")

    def testStrokeNoneEncodesAsZero(self):
        self.assertEqual(codeInfo("60x0").code, "6000")

    def testReferencedCornerEncodesAsZero(self):
        # 已被其他角使用的筆形，再被引用時取 0
        corners = (FCStroke.Stroke3, FCCorner.TopLeft, FCStroke.Stroke8, FCCorner.BottomLeft)
        codeInfoRef = FCCodeInfo(FCLump(corners))

        self.assertEqual(codeInfoRef.code, "3080")

    def testInnerLumpUsesTopOfOuterAndBottomOfInner(self):
        # 全包結構：外框取上方兩角，內含物取下方兩角
        outer = lump("6666")
        inner = lump("1234")

        self.assertEqual(FCCodeInfo(outer, inner).code, "6634")


class FCCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = FCCodeInfoEncoder()

    def encode(self, operator, codeInfoList):
        return self.encoder.setByComps(operator, codeInfoList).code

    def testEncodeAsEqual(self):
        self.assertEqual(self.encode(Operator.Equal, [codeInfo("7722")]), "7722")

    def testEncodeAsSilkworm(self):
        # 蚕：上部件取上兩角，下部件取下兩角
        code = self.encode(Operator.Silkworm, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1278")

    def testEncodeAsGoose(self):
        # 鴻：左部件取左兩角，右部件取右兩角
        code = self.encode(Operator.Goose, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1638")

    def testEncodeAsLoopWithFrame(self):
        # 回：外框可透視時，取外框上兩角與內含物下兩角
        code = self.encode(
            Operator.Loop, [codeInfo("6666", sl=True), codeInfo("1234")]
        )
        self.assertEqual(code, "6634")

    def testEncodeAsLoopWithoutFrame(self):
        # 回：外框不可透視時，只取外框
        code = self.encode(Operator.Loop, [codeInfo("6666"), codeInfo("1234")])
        self.assertEqual(code, "6666")

    def testEncodeAsQi(self):
        # 起：內含物取右上角
        code = self.encode(Operator.Qi, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1634")

    def testEncodeAsLiao(self):
        # 廖：內含物取右下角
        code = self.encode(Operator.Liao, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1238")

    def testEncodeAsZai(self):
        # 載：內含物取左下角
        code = self.encode(Operator.Zai, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1274")

    def testEncodeAsDou(self):
        # 斗：內含物取左上角
        code = self.encode(Operator.Dou, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "5234")

    def testEncodeAsMu(self):
        # 畞：上部件取上兩角，下部件取左下、右下角
        code = self.encode(Operator.Mu, [codeInfo("1234"), codeInfo("5678")])
        self.assertEqual(code, "1278")

    def testEncodeAsZuo(self):
        # 㘴：兩個上部件各取左上、右上角，下部件取下兩角
        code = self.encode(
            Operator.Zuo, [codeInfo("1234"), codeInfo("5678"), codeInfo("9012")]
        )
        self.assertEqual(code, "5034")

    def testEncodeAsYouKeepsFirstComponent(self):
        code = self.encode(
            Operator.You, [codeInfo("1234"), codeInfo("5678"), codeInfo("9012")]
        )
        self.assertEqual(code, "1234")


if __name__ == "__main__":
    unittest.main()
