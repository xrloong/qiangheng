import tempfile
import unittest
from pathlib import Path

import ruamel.yaml

from element.enum import CodeVariance
from element.enum import FontVariance
from parser.QHParser import QHParser


class QHParserTestCase(unittest.TestCase):
    def setUp(self):
        self.tempDir = tempfile.TemporaryDirectory()
        self.parser = QHParser(yaml=ruamel.yaml.YAML(typ="safe"))

    def tearDown(self):
        self.tempDir.cleanup()

    def writeYaml(self, content):
        path = Path(self.tempDir.name) / "data.yaml"
        path.write_text(content)
        return str(path)

    def testLoadSubstituteRuleSet(self):
        filename = self.writeYaml(
            """規則集:
  - 比對: "({運算=同} ({名稱=戌}) .)"
    替換: "(同 戊 (蚕 一 \\\\2))"
  - 比對:
      運算: "蚕"
      參數個數: 3
    替換: "(蚕 \\\\1 \\\\2 \\\\3)"
"""
        )

        ruleSet = self.parser.loadSubstituteRuleSet(filename)

        self.assertEqual(len(ruleSet.rules), 2)
        self.assertEqual(ruleSet.rules[0].matching, "({運算=同} ({名稱=戌}) .)")
        self.assertEqual(ruleSet.rules[1].matching.operator, "蚕")
        self.assertEqual(ruleSet.rules[1].matching.operandCount, 3)

    def testLoadRadicalSet(self):
        filename = self.writeYaml(
            """字符集:
  - 名稱: "一"
    註記: "U+4E00"
    編碼資訊:
      - 編碼表示式: '*m'
  - 名稱: "七"
    註記: "U+4E03"
    編碼資訊:
      - 編碼表示式: '*p'
      - 類型: '容錯'
        編碼表示式: '*ju'
"""
        )

        radicalSet = self.parser.loadRadicalSet(filename)

        self.assertEqual(len(radicalSet.radicals), 2)

        radical七 = radicalSet.radicals[1]
        self.assertEqual(radical七.name, "七")
        self.assertEqual(radical七.codings[0].variance, CodeVariance.STANDARD)
        self.assertEqual(radical七.codings[1].variance, CodeVariance.TOLERANT)

    def testLoadCharacterDecompositionSet(self):
        filename = self.writeYaml(
            """字符集:
  - 名稱: "瑲"
    註記: "U+7472"
    結構集:
    - {結構: "({運算=鴻}({置換=王})({置換=倉}))"}
  - 名稱: "廏"
    註記: "U+5ECF"
    結構集:
    - {結構: "({運算=爲}({置換=[廏下]}))", 字體: "傳"}
    - {結構: "({運算=爲}({置換=[廄下]}))", 字體: "簡"}
"""
        )

        decompositionSet = self.parser.loadCharacterDecompositionSet(filename)

        self.assertEqual(len(decompositionSet.decompositionSet), 2)

        decomposition瑲 = decompositionSet.decompositionSet[0]
        self.assertEqual(decomposition瑲.name, "瑲")
        self.assertEqual(decomposition瑲.structureSet[0].font, FontVariance.All)

        decomposition廏 = decompositionSet.decompositionSet[1]
        self.assertEqual(decomposition廏.structureSet[0].font, FontVariance.Traditional)
        self.assertEqual(decomposition廏.structureSet[1].font, FontVariance.Simplified)


if __name__ == "__main__":
    unittest.main()
