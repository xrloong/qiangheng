import functools
import unittest

from coding.Base.interface import IfCodeInfo, IfCodeInfoEncoder, IfCodingRadixParser
from coding.Input import InputPlugin, FontVariance
from coding.Input.Input import CodeMappingInfoInterpreter as InputInterpreter
from coding.Drawing import DrawingPlugin
from coding.Drawing.Drawing import CodeMappingInfoInterpreter as DrawingInterpreter


# ── stub classes ────────────────────────────────────────────────────────────


class StubEncoder:
    pass


class StubParser:
    pass


class StubInterpreter(DrawingInterpreter):
    pass


# ── abstract interface enforcement ──────────────────────────────────────────


class InterfaceContractTestCase(unittest.TestCase):
    def testIfCodeInfoCannotBeInstantiated(self):
        with self.assertRaises(TypeError):
            IfCodeInfo()

    def testIfCodeInfoEncoderCannotBeInstantiated(self):
        with self.assertRaises(TypeError):
            IfCodeInfoEncoder()

    def testIfCodingRadixParserCannotBeInstantiated(self):
        with self.assertRaises(TypeError):
            IfCodingRadixParser()

    def testConcreteSubclassWithCodePropertyIsInstantiable(self):
        class ConcreteCodeInfo(IfCodeInfo):
            @property
            def code(self):
                return "x"

        obj = ConcreteCodeInfo()
        self.assertEqual(obj.code, "x")

    def testConcreteSubclassMissingCodePropertyRaises(self):
        class Incomplete(IfCodeInfo):
            pass

        with self.assertRaises(TypeError):
            Incomplete()


# ── InputPlugin ─────────────────────────────────────────────────────────────


class InputPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.plugin = InputPlugin(
            method_name="ar",
            encoder_class=StubEncoder,
            radix_parser_class=StubParser,
            font_variance=FontVariance.Traditional,
        )

    def testMethodDir(self):
        self.assertEqual(self.plugin._method_dir, "gen/qhdata/ar/")

    def testCodeInfoEncoderReturnsClass(self):
        self.assertIs(self.plugin.CodeInfoEncoder, StubEncoder)

    def testCodingRadixParserReturnsClass(self):
        self.assertIs(self.plugin.CodingRadixParser, StubParser)

    def testFontVariance(self):
        self.assertEqual(self.plugin.fontVariance, FontVariance.Traditional)

    def testCodeMappingInfoInterpreterIsInputInterpreter(self):
        self.assertIsInstance(self.plugin.codeMappingInfoInterpreter, InputInterpreter)

    def testCodingSubstituteFileList(self):
        self.assertEqual(
            self.plugin.CodingSubstituteFileList,
            ["gen/qhdata/ar/substitute.yaml"],
        )

    def testCodingRadixFileList(self):
        self.assertEqual(
            self.plugin.CodingRadixFileList,
            [
                "gen/qhdata/ar/radix/CJK.yaml",
                "gen/qhdata/ar/radix/CJK-A.yaml",
            ],
        )

    def testCodingAdjustFileList(self):
        self.assertEqual(
            self.plugin.CodingAdjustFileList,
            ["gen/qhdata/ar/adjust.yaml"],
        )

    def testCodingFastFileRaisesWhenNotEnabled(self):
        with self.assertRaises(AttributeError):
            _ = self.plugin.CodingFastFile

    def testCodingFastFileReturnPathWhenEnabled(self):
        plugin = InputPlugin(
            method_name="bs",
            encoder_class=StubEncoder,
            radix_parser_class=StubParser,
            has_fast_file=True,
        )
        self.assertEqual(plugin.CodingFastFile, "gen/qhdata/bs/fast.yaml")

    def testCustomMethodDirOverridesDerivedPaths(self):
        plugin = InputPlugin(
            method_name="gx",
            encoder_class=StubEncoder,
            radix_parser_class=StubParser,
            method_dir="samples/GuiXie/qhdata/",
        )
        self.assertEqual(plugin._method_dir, "samples/GuiXie/qhdata/")
        self.assertEqual(
            plugin.CodingSubstituteFileList,
            ["samples/GuiXie/qhdata/substitute.yaml"],
        )
        self.assertEqual(
            plugin.CodingRadixFileList,
            [
                "samples/GuiXie/qhdata/radix/CJK.yaml",
                "samples/GuiXie/qhdata/radix/CJK-A.yaml",
            ],
        )
        self.assertEqual(
            plugin.CodingAdjustFileList,
            ["samples/GuiXie/qhdata/adjust.yaml"],
        )

    def testSimplifiedFontVariance(self):
        plugin = InputPlugin(
            method_name="zm",
            encoder_class=StubEncoder,
            radix_parser_class=StubParser,
            font_variance=FontVariance.Simplified,
        )
        self.assertEqual(plugin.fontVariance, FontVariance.Simplified)


# ── DrawingPlugin ────────────────────────────────────────────────────────────


class DrawingPluginTestCase(unittest.TestCase):
    def setUp(self):
        self.interpreter = StubInterpreter()
        self.plugin = DrawingPlugin(
            method_name="dc",
            encoder_class=StubEncoder,
            radix_parser_class=StubParser,
            interpreter=self.interpreter,
            font_variance=FontVariance.Traditional,
        )

    def testMethodDir(self):
        self.assertEqual(self.plugin._method_dir, "gen/qhdata/dc/")

    def testCodeInfoEncoderReturnsClass(self):
        self.assertIs(self.plugin.CodeInfoEncoder, StubEncoder)

    def testCodingRadixParserReturnsPartialBoundToTemplateFile(self):
        parser = self.plugin.CodingRadixParser
        self.assertIsInstance(parser, functools.partial)
        self.assertIs(parser.func, StubParser)
        self.assertEqual(parser.args, (self.plugin.CodingTemplateFile,))

    def testFontVariance(self):
        self.assertEqual(self.plugin.fontVariance, FontVariance.Traditional)

    def testCodeMappingInfoInterpreterIsPassedInterpreter(self):
        self.assertIs(self.plugin.codeMappingInfoInterpreter, self.interpreter)

    def testCodingSubstituteFileList(self):
        self.assertEqual(
            self.plugin.CodingSubstituteFileList,
            ["gen/qhdata/dc/substitute.yaml"],
        )

    def testCodingRadixFileList(self):
        self.assertEqual(
            self.plugin.CodingRadixFileList,
            [
                "gen/qhdata/dc/radix/CJK.yaml",
                "gen/qhdata/dc/radix/CJK-A.yaml",
            ],
        )

    def testCodingAdjustFileList(self):
        self.assertEqual(
            self.plugin.CodingAdjustFileList,
            ["gen/qhdata/dc/adjust.yaml"],
        )

    def testCodingTemplateFile(self):
        self.assertEqual(
            self.plugin.CodingTemplateFile,
            "gen/qhdata/dc/radix/template.yaml",
        )


if __name__ == "__main__":
    unittest.main()
