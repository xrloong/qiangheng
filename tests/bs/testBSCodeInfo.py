import unittest

from coding.Boshiamy.Boshiamy import BSCodeInfo
from coding.Boshiamy.Boshiamy import BSCodeInfoEncoder
from element.operator import Operator


class BSCodeInfoTestCase(unittest.TestCase):
    # 嘸蝦米規則：
    # 1 拆碼超過四碼時，取首、次、三、尾碼
    # 2 拆碼不足三碼時，需加補碼
    # 2-1 一到十等數目的字不用加補碼

    def testCodeIsNoneWithoutCodeSequence(self):
        codeInfo = BSCodeInfo(None, None, False)
        self.assertIsNone(codeInfo.code)

    def testShortCodeAppendsSupplement(self):
        # 規則 2
        codeInfo = BSCodeInfo(["a"], "v", False)
        self.assertEqual(codeInfo.code, "av")

        codeInfo = BSCodeInfo(["a", "b"], "v", False)
        self.assertEqual(codeInfo.code, "abv")

    def testShortCodeWithoutSupplementIsNone(self):
        codeInfo = BSCodeInfo(["a"], None, False)
        self.assertIsNone(codeInfo.code)

    def testShortCodeIgnoringSupplement(self):
        # 規則 2-1
        codeInfo = BSCodeInfo(["o"], None, True)
        self.assertEqual(codeInfo.code, "o")

    def testMediumCodeIsUnchanged(self):
        codeInfo = BSCodeInfo(["a", "b", "c"], "v", False)
        self.assertEqual(codeInfo.code, "abc")

        codeInfo = BSCodeInfo(["a", "b", "c", "d"], "v", False)
        self.assertEqual(codeInfo.code, "abcd")

    def testLongCodeIsTruncated(self):
        # 規則 1
        codeInfo = BSCodeInfo(["a", "b", "c", "d", "e"], "v", False)
        self.assertEqual(codeInfo.code, "abce")

        codeInfo = BSCodeInfo(["a", "b", "c", "d", "e", "f"], "v", False)
        self.assertEqual(codeInfo.code, "abcf")


class BSCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = BSCodeInfoEncoder()

    def codeInfo(self, codeSequence, supplementCode=None):
        return BSCodeInfo(codeSequence, supplementCode, False)

    def testEncodeAsLoongConcatenatesSequences(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(["a", "b"]), self.codeInfo(["c"], "v")],
        )

        self.assertEqual(codeInfo.codeSequence, ["a", "b", "c"])
        self.assertEqual(codeInfo.supplementCode, "v")

    def testEncodeAsLoongTruncatesLongSequences(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(["a", "b", "c"]), self.codeInfo(["d", "e"], "v")],
        )

        self.assertEqual(codeInfo.codeSequence, ["a", "b", "c", "e"])

    def testSupplementComesFromLastComponent(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(["a"], "x"), self.codeInfo(["b"], "y")],
        )

        self.assertEqual(codeInfo.supplementCode, "y")

    def testGooseFallsBackToLoong(self):
        codeInfo = self.encoder.setByComps(
            Operator.Goose,
            [self.codeInfo(["a"]), self.codeInfo(["b"], "v")],
        )

        self.assertEqual(codeInfo.codeSequence, ["a", "b"])

    def testEncodeAsHanSwapsOperands(self):
        # 函：外框後取，先取被包的部件
        codeInfo = self.encoder.setByComps(
            Operator.Han,
            [self.codeInfo(["a"], "x"), self.codeInfo(["b", "c"], "y")],
        )

        self.assertEqual(codeInfo.codeSequence, ["b", "c", "a"])
        self.assertEqual(codeInfo.supplementCode, "x")

    def testEncodeAsZheSwapsOperands(self):
        # 這：辶後取
        codeInfo = self.encoder.setByComps(
            Operator.Zhe,
            [self.codeInfo(["a"], "x"), self.codeInfo(["b"], "y")],
        )

        self.assertEqual(codeInfo.codeSequence, ["b", "a"])

    def testEncodeAsYouRotatesOperands(self):
        # 幽：山最後取
        codeInfo = self.encoder.setByComps(
            Operator.You,
            [
                self.codeInfo(["a"], "x"),
                self.codeInfo(["b"], "y"),
                self.codeInfo(["c"], "z"),
            ],
        )

        self.assertEqual(codeInfo.codeSequence, ["b", "c", "a"])
        self.assertEqual(codeInfo.supplementCode, "x")

    def testOperationUnavailableWhenComponentHasNoCode(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong,
            [self.codeInfo(["a"]), self.codeInfo(None)],
        )

        self.assertIsNone(codeInfo)


if __name__ == "__main__":
    unittest.main()
