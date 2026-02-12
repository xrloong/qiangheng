import unittest

from coding.Base import truncateCode


class TruncateCodeTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTruncateCodeShortSequence(self):
        """Test that sequences shorter than max_len are returned unchanged."""
        seq = "abc"
        result = truncateCode(seq)
        self.assertEqual(result, "abc")

    def testTruncateCodeEqualToMaxLen(self):
        """Test that sequences equal to max_len are returned unchanged."""
        seq = "abcd"
        result = truncateCode(seq)
        self.assertEqual(result, "abcd")

    def testTruncateCodeExceedsMaxLen(self):
        """Test that sequences longer than max_len are truncated correctly."""
        seq = "abcde"
        result = truncateCode(seq)
        # Keep first 3 (head_len=3) and last 1 (max_len - head_len = 4 - 3 = 1)
        self.assertEqual(result, "abce")

    def testTruncateCodeLongSequence(self):
        """Test truncation of longer sequences."""
        seq = "abcdefgh"
        result = truncateCode(seq)
        # Keep first 3 and last 1
        self.assertEqual(result, "abch")

    def testTruncateCodeCustomMaxLen(self):
        """Test truncation with custom max_len parameter."""
        seq = "abcdef"
        result = truncateCode(seq, max_len=5)
        # Keep first 3 (default head_len=3) and last 2 (5 - 3 = 2)
        self.assertEqual(result, "abcef")

    def testTruncateCodeCustomHeadLen(self):
        """Test truncation with custom head_len parameter."""
        seq = "abcdef"
        result = truncateCode(seq, max_len=4, head_len=2)
        # Keep first 2 and last 2 (4 - 2 = 2)
        self.assertEqual(result, "abef")

    def testTruncateCodeEmptySequence(self):
        """Test that empty sequences are handled correctly."""
        seq = ""
        result = truncateCode(seq)
        self.assertEqual(result, "")

    def testTruncateCodeSingleElement(self):
        """Test sequences with single element."""
        seq = "a"
        result = truncateCode(seq)
        self.assertEqual(result, "a")

    def testTruncateCodeWithTuple(self):
        """Test truncation works with tuples."""
        seq = (1, 2, 3, 4, 5)
        result = truncateCode(seq, max_len=4, head_len=2)
        # Keep first 2 and last 2
        self.assertEqual(result, (1, 2, 4, 5))

    def testTruncateCodeWithList(self):
        """Test truncation works with lists."""
        seq = [1, 2, 3, 4, 5]
        result = truncateCode(seq, max_len=4, head_len=2)
        # Keep first 2 and last 2
        self.assertEqual(result, [1, 2, 4, 5])


if __name__ == "__main__":
    unittest.main()
