import tempfile
import unittest
from pathlib import Path

from parser.GlyphParser import GlyphParser
from parser.GlyphParser import GlyphTags


class GlyphElementParsingTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = GlyphParser()

    def testParseDefinitionElement(self):
        element = self.parser.parseElement(
            {
                "方式": "定義",
                "類型": "橫",
                "樣條節點串列": [[[202, 0]]],
                "起始點": [20, 123],
                "定位": [20, 123, 222, 123],
            }
        )

        self.assertTrue(element.isDefinition)
        self.assertFalse(element.isReference)
        self.assertFalse(element.isAnchor)

        self.assertEqual(element.strokeType, "橫")
        self.assertEqual(element.splinePointsList, [[[202, 0]]])
        self.assertEqual(element.startPoint, [20, 123])
        self.assertEqual(element.position, [20, 123, 222, 123])
        self.assertIsNone(element.params)

    def testParseReferenceElement(self):
        element = self.parser.parseElement(
            {"方式": "引用", "引用名稱": "~點", "順序": 0, "定位": [93, 91, 153, 164]}
        )

        self.assertTrue(element.isReference)
        self.assertFalse(element.isDefinition)
        self.assertFalse(element.isAnchor)

        self.assertEqual(element.referenceName, "~點")
        self.assertEqual(element.order, 0)
        self.assertEqual(element.position, [93, 91, 153, 164])

    def testParseReferenceElementWithoutOrder(self):
        # 省略「順序」時，代表依序使用所引用部件的全部筆劃
        element = self.parser.parseElement({"方式": "引用", "引用名稱": "#一"})

        self.assertTrue(element.isReference)
        self.assertIsNone(element.order)
        self.assertIsNone(element.position)

    def testParseAnchorElement(self):
        element = self.parser.parseElement(
            {"方式": "錨點", "名稱": "上", "引用名稱": "@一"}
        )

        self.assertTrue(element.isAnchor)
        self.assertFalse(element.isDefinition)
        self.assertFalse(element.isReference)

        self.assertEqual(element.name, "上")
        self.assertEqual(element.referenceName, "@一")
        self.assertIsNone(element.position)

    def testParseUnknownMethod(self):
        element = self.parser.parseElement({"方式": "未知"})

        self.assertFalse(element.isDefinition)
        self.assertFalse(element.isReference)
        self.assertFalse(element.isAnchor)


class GlyphParserLoadTestCase(unittest.TestCase):
    def setUp(self):
        self.tempDir = tempfile.TemporaryDirectory()
        self.parser = GlyphParser()

    def tearDown(self):
        self.tempDir.cleanup()

    def writeYaml(self, content):
        path = Path(self.tempDir.name) / "glyph.yaml"
        path.write_text(content)
        return str(path)

    def testLoadDataSet(self):
        filename = self.writeYaml(
            """---
筆劃集:
  - 名稱: "~點"
    註記: 衣 主 沙
    筆劃: {方式: 定義, 類型: 點, 樣條節點串列: [[[60, 73]]], 起始點: [93, 91], 定位: [93, 91, 153, 164]}
零件集:
  - 名稱: "#丶"
    筆劃:
      - {方式: 引用, 引用名稱: "~點"}
部件集:
  - 名稱: "@二"
    註記: 二
    筆劃:
      - {方式: 引用, 引用名稱: "#一", 定位: [20, 40, 222, 40]}
      - {方式: 引用, 引用名稱: "#一", 定位: [20, 180, 222, 180]}
"""
        )

        dataSet = self.parser.load(filename)

        self.assertEqual(len(dataSet.strokes), 1)
        self.assertEqual(len(dataSet.parts), 1)
        self.assertEqual(len(dataSet.components), 1)

        stroke = dataSet.strokes[0]
        self.assertEqual(stroke.name, "~點")
        self.assertEqual(stroke.comment, "衣 主 沙")
        self.assertTrue(stroke.element.isDefinition)
        self.assertEqual(stroke.element.strokeType, "點")

        part = dataSet.parts[0]
        self.assertEqual(part.name, "#丶")
        self.assertIsNone(part.comment)
        self.assertEqual(len(part.elements), 1)
        self.assertTrue(part.elements[0].isReference)
        self.assertEqual(part.elements[0].referenceName, "~點")

        component = dataSet.components[0]
        self.assertEqual(component.name, "@二")
        self.assertEqual(component.comment, "二")
        self.assertEqual(len(component.elements), 2)
        self.assertEqual(component.elements[0].position, [20, 40, 222, 40])
        self.assertEqual(component.elements[1].position, [20, 180, 222, 180])


class GlyphTagsTestCase(unittest.TestCase):
    def testMethodTags(self):
        self.assertEqual(GlyphTags.METHOD__DEFINITION, "定義")
        self.assertEqual(GlyphTags.METHOD__REFERENCE, "引用")
        self.assertEqual(GlyphTags.METHOD__ANCHOR, "錨點")


if __name__ == "__main__":
    unittest.main()
