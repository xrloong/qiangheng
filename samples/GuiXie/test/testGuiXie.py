import unittest


class GuiXieTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ImportGuiXie(self):
        try:
            pass
        except:
            self.fail("coding.GuiXie 不存在。")

    def test_plugin_exists(self):
        try:
            from coding.GuiXie import plugin  # noqa: F401
        except ImportError:
            self.fail("coding.GuiXie 中缺少 plugin")

    def test_CodingSubstituteFileList_exists(self):
        from coding.GuiXie import plugin

        for f in plugin.CodingSubstituteFileList:
            # 確認檔案存在
            try:
                open(f, "r").close()
            except FileNotFoundError:
                self.fail("{} 不存在".format(f))

    def test_CodingRadixFileList_exists(self):
        from coding.GuiXie import plugin

        for f in plugin.CodingRadixFileList:
            # 確認檔案存在
            try:
                open(f, "r").close()
            except FileNotFoundError:
                self.fail("{} 不存在".format(f))

    def test_fontVariance_exists(self):
        from coding.GuiXie import plugin
        from element.enum import FontVariance

        self.assertIsInstance(plugin.fontVariance, FontVariance)

    def test_codeMappingInfoInterpreter_exists(self):
        from coding.GuiXie import plugin

        self.assertIsNotNone(plugin.codeMappingInfoInterpreter)
