import unittest

from coding.DaYi.DaYi import DYCodeInfo
from coding.DaYi.DaYi import DYCodeInfoEncoder
from element.operator import Operator


class DYCodeInfoTestCase(unittest.TestCase):
    def testShortCodeIsUnchanged(self):
        self.assertEqual(DYCodeInfo("a").code, "a")
        self.assertEqual(DYCodeInfo("ab").code, "ab")
        self.assertEqual(DYCodeInfo("abcd").code, "abcd")

    def testLongCodeIsTruncated(self):
        # 超過四碼時，取首、次、三、尾碼
        self.assertEqual(DYCodeInfo("abcde").code, "abce")
        self.assertEqual(DYCodeInfo("abcdef").code, "abcf")

    def testSymbolRadices(self):
        # 大易字根含數字與符號，其中「:」字根輸出為「,」
        self.assertEqual(DYCodeInfo("0v").code, "0v")
        self.assertEqual(DYCodeInfo(".;/").code, ".;/")
        self.assertEqual(DYCodeInfo(":").code, ",")


class DYCodeInfoEncoderTestCase(unittest.TestCase):
    def setUp(self):
        self.encoder = DYCodeInfoEncoder()

    def testEncodeAsLoongConcatenatesCodes(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong, [DYCodeInfo("ab"), DYCodeInfo("c")]
        )

        self.assertEqual(codeInfo.code, "abc")

    def testEncodeAsLoongTruncatesLongCodes(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong, [DYCodeInfo("abc"), DYCodeInfo("de")]
        )

        self.assertEqual(codeInfo.code, "abce")

    def testGooseFallsBackToLoong(self):
        codeInfo = self.encoder.setByComps(
            Operator.Goose, [DYCodeInfo("a"), DYCodeInfo("b")]
        )

        self.assertEqual(codeInfo.code, "ab")

    def testEncodeAsHanSwapsOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.Han, [DYCodeInfo("a"), DYCodeInfo("bc")]
        )

        self.assertEqual(codeInfo.code, "bca")

    def testEncodeAsZheSwapsOperands(self):
        codeInfo = self.encoder.setByComps(
            Operator.Zhe, [DYCodeInfo("a"), DYCodeInfo("b")]
        )

        self.assertEqual(codeInfo.code, "ba")

    def testEncodeAsLuanRepeatsSecondOperand(self):
        codeInfo = self.encoder.setByComps(
            Operator.Luan, [DYCodeInfo("x"), DYCodeInfo("y")]
        )

        self.assertEqual(codeInfo.code, "xyy")

    def testOperationUnavailableWhenComponentHasNoCode(self):
        codeInfo = self.encoder.setByComps(
            Operator.Loong, [DYCodeInfo("a"), DYCodeInfo(())]
        )

        self.assertIsNone(codeInfo)


if __name__ == "__main__":
    unittest.main()
