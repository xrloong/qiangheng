import unittest

from element.enum import CodeVariance
from model.element.CharacterDescription import CharacterDescription
from model.element.CharacterDescription import CharacterDecompositionSet
from model.element.CodeMappingInfo import CodeMappingInfo
from parser.model import CharacterDecompositionModel
from parser.model import CharacterDecompositionSetModel


class CodeMappingInfoTestCase(unittest.TestCase):
    def testGetters(self):
        info = CodeMappingInfo("瑲", "mgoiv", CodeVariance.STANDARD)

        self.assertEqual(info.getName(), "瑲")
        self.assertEqual(info.getCode(), "mgoiv")
        self.assertEqual(info.getVariance(), CodeVariance.STANDARD)

    def testKeyOrderIsCodeNameVariance(self):
        info = CodeMappingInfo("瑲", "mgoiv", CodeVariance.STANDARD)

        self.assertEqual(info.getKey(), ["mgoiv", "瑲", CodeVariance.STANDARD])


class CharacterDescriptionTestCase(unittest.TestCase):
    def testFromName(self):
        charDesc = CharacterDescription(name="一")

        self.assertEqual(charDesc.name, "一")
        self.assertEqual(charDesc.structures, ())

    def testFromModel(self):
        model = CharacterDecompositionModel(
            名稱="瑲",
            註記="U+7472",
            結構集=[{"結構": "({運算=鴻}({置換=王})({置換=倉}))"}],
        )
        charDesc = CharacterDescription(model=model)

        self.assertEqual(charDesc.name, "瑲")
        # 結構需經 prepareStructures 轉換後才可用
        self.assertIsNone(charDesc.structures)


class CharacterDecompositionSetTestCase(unittest.TestCase):
    def testCharDescs(self):
        model = CharacterDecompositionSetModel(
            字符集=[
                {"名稱": "一", "註記": "U+4E00", "結構集": [{"結構": "()"}]},
                {"名稱": "二", "註記": "U+4E8C", "結構集": [{"結構": "(蚕 一 一)"}]},
            ]
        )
        decompositionSet = CharacterDecompositionSet(model)

        names = [charDesc.name for charDesc in decompositionSet.charDescs]
        self.assertEqual(names, ["一", "二"])


if __name__ == "__main__":
    unittest.main()
