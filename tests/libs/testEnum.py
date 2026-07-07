import unittest

from element.enum import CodeVariance
from element.enum import FontVariance


class FontVarianceTestCase(unittest.TestCase):
    def testValues(self):
        self.assertEqual(FontVariance.All, "全")
        self.assertEqual(FontVariance.Traditional, "傳")
        self.assertEqual(FontVariance.Simplified, "簡")

    def testAllContainsEverything(self):
        self.assertTrue(FontVariance.All.contains(FontVariance.All))
        self.assertTrue(FontVariance.All.contains(FontVariance.Traditional))
        self.assertTrue(FontVariance.All.contains(FontVariance.Simplified))

    def testTraditionalContainsAllAndTraditional(self):
        self.assertTrue(FontVariance.Traditional.contains(FontVariance.All))
        self.assertTrue(FontVariance.Traditional.contains(FontVariance.Traditional))
        self.assertFalse(FontVariance.Traditional.contains(FontVariance.Simplified))

    def testSimplifiedContainsAllAndSimplified(self):
        self.assertTrue(FontVariance.Simplified.contains(FontVariance.All))
        self.assertTrue(FontVariance.Simplified.contains(FontVariance.Simplified))
        self.assertFalse(FontVariance.Simplified.contains(FontVariance.Traditional))


class CodeVarianceTestCase(unittest.TestCase):
    def testValues(self):
        self.assertEqual(CodeVariance.STANDARD, "標準")
        self.assertEqual(CodeVariance.SIMPLIFIED, "簡快")
        self.assertEqual(CodeVariance.TOLERANT, "容錯")

    def testIntValue(self):
        self.assertEqual(CodeVariance.STANDARD.intValue, 0)
        self.assertEqual(CodeVariance.SIMPLIFIED.intValue, 1)
        self.assertEqual(CodeVariance.TOLERANT.intValue, 2)

    def testMultiplyIsIdempotent(self):
        self.assertEqual(
            CodeVariance.STANDARD * CodeVariance.STANDARD, CodeVariance.STANDARD
        )
        self.assertEqual(
            CodeVariance.SIMPLIFIED * CodeVariance.SIMPLIFIED, CodeVariance.SIMPLIFIED
        )
        self.assertEqual(
            CodeVariance.TOLERANT * CodeVariance.TOLERANT, CodeVariance.TOLERANT
        )

    def testMultiplyKeepsHigherVariance(self):
        self.assertEqual(
            CodeVariance.STANDARD * CodeVariance.SIMPLIFIED, CodeVariance.SIMPLIFIED
        )
        self.assertEqual(
            CodeVariance.STANDARD * CodeVariance.TOLERANT, CodeVariance.TOLERANT
        )
        self.assertEqual(
            CodeVariance.SIMPLIFIED * CodeVariance.TOLERANT, CodeVariance.TOLERANT
        )

    def testMultiplyIsCommutative(self):
        self.assertEqual(
            CodeVariance.SIMPLIFIED * CodeVariance.STANDARD, CodeVariance.SIMPLIFIED
        )
        self.assertEqual(
            CodeVariance.TOLERANT * CodeVariance.STANDARD, CodeVariance.TOLERANT
        )
        self.assertEqual(
            CodeVariance.TOLERANT * CodeVariance.SIMPLIFIED, CodeVariance.TOLERANT
        )


if __name__ == "__main__":
    unittest.main()
