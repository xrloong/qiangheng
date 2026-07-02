import io
import unittest

import ruamel.yaml

from fastyaml import FastYamlDumper
from fastyaml import FallbackNeeded


def ruamelDump(data):
    yaml = ruamel.yaml.YAML(typ="safe", pure=True)
    yaml.explicit_start = True
    yaml.explicit_end = True
    yaml.allow_unicode = True
    yaml.default_flow_style = False
    buf = io.StringIO()
    yaml.dump(data, buf)
    return buf.getvalue()


class FastYamlDumperTestCase(unittest.TestCase):
    def setUp(self):
        self.dumper = FastYamlDumper()

    def assertMatchesRuamel(self, data):
        self.assertEqual(self.dumper.dumps(data), ruamelDump(data))

    def testCodeMappingShape(self):
        data = {
            "編碼類型": "描繪法",
            "編碼集": [
                {
                    "字圖": [
                        {"名稱": "橫", "描繪": "0.20.124,1.96.124"},
                        {"名稱": "豎", "描繪": "0.96.17,1.96.233"},
                    ],
                    "字符": "㐀",
                    "類型": "標準",
                },
                {"字符": "㐁", "類型": "標準", "編碼": "abcd"},
            ],
        }
        self.assertMatchesRuamel(data)

    def testKeysAreSorted(self):
        data = {"乙": "b", "甲": "a", "丙": {"丁": "d", "戊": "e"}}
        self.assertMatchesRuamel(data)

    def testNumericStringsAreQuoted(self):
        data = {
            "編碼集": [
                {"字符": "㐀", "按鍵序列": "1110"},
                {"字符": "㐁", "按鍵序列": "4071"},
                {"字符": "㐂", "按鍵序列": "1.5"},
                {"字符": "㐃", "按鍵序列": "0x1f"},
            ]
        }
        self.assertMatchesRuamel(data)

    def testSequenceOfStrings(self):
        data = {"編碼集": ["abc", "1234", "字串"]}
        self.assertMatchesRuamel(data)

    def testLongQuotedScalarStaysInline(self):
        # 無空白的單引號字串不折行
        for length in range(60, 96):
            value = "0." + "1" * length
            data = {"編碼集": [{"字圖": [{"名稱": "橫", "描繪": value}]}]}
            self.assertMatchesRuamel(data)

    def testLongScalarWrapBoundary(self):
        # 掃過換行門檻，確保折行行為與 ruamel 一致（多個小數點 → plain 字串）
        for length in range(60, 96):
            value = "0.128.207," * (length // 10) + "1" * (length % 10 + 1)
            data = {
                "編碼集": [
                    {
                        "字圖": [{"名稱": "橫", "描繪": value}],
                        "字符": "㐀",
                        "類型": "標準",
                    }
                ]
            }
            self.assertMatchesRuamel(data)

    def testTopLevelLongScalarWrapBoundary(self):
        for length in range(60, 96):
            value = "x" * length
            self.assertMatchesRuamel({"編碼": value, "字符": "㐀"})

    def testFallbackOnUnsupportedData(self):
        cases = [
            {"字符": "a b"},  # 含空白的字串
            {"字符": ""},  # 空字串
            {"字符": "a\nb"},  # 多行字串
            {"字符": 123},  # 非字串葉值
            {"字符": None},
            {"字符": []},  # 空容器
            {"字符": {}},
            {},
        ]
        for data in cases:
            with self.assertRaises(FallbackNeeded):
                self.dumper.dumps(data)
