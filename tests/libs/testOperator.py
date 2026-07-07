import unittest

from element.operator import Operator


class OperatorTestCase(unittest.TestCase):
    def testName(self):
        operator = Operator("龜")
        self.assertEqual(operator.name, "龜")

    def testStr(self):
        operator = Operator("鴻")
        self.assertEqual(str(operator), "鴻")

    def testEquality(self):
        self.assertEqual(Operator("龜"), Operator("龜"))
        self.assertEqual(Operator("龜"), Operator.Turtle)

    def testInequality(self):
        self.assertNotEqual(Operator("龜"), Operator("龍"))
        self.assertNotEqual(Operator.Turtle, Operator.Loong)

    def testGenerateBuiltin(self):
        operator = Operator.generateBuiltin("回")
        self.assertEqual(operator, Operator.Loop)

    def testBuiltinNames(self):
        self.assertEqual(Operator.Turtle.name, "龜")
        self.assertEqual(Operator.Loong.name, "龍")
        self.assertEqual(Operator.Sparrow.name, "雀")
        self.assertEqual(Operator.Equal.name, "爲")

        self.assertEqual(Operator.Silkworm.name, "蚕")
        self.assertEqual(Operator.Goose.name, "鴻")
        self.assertEqual(Operator.Loop.name, "回")

        self.assertEqual(Operator.Qi.name, "起")
        self.assertEqual(Operator.Zhe.name, "這")
        self.assertEqual(Operator.Liao.name, "廖")
        self.assertEqual(Operator.Zai.name, "載")
        self.assertEqual(Operator.Dou.name, "斗")

        self.assertEqual(Operator.Tong.name, "同")
        self.assertEqual(Operator.Han.name, "函")
        self.assertEqual(Operator.Qu.name, "區")
        self.assertEqual(Operator.Left.name, "左")

        self.assertEqual(Operator.Mu.name, "畞")
        self.assertEqual(Operator.Zuo.name, "㘴")
        self.assertEqual(Operator.You.name, "幽")
        self.assertEqual(Operator.Liang.name, "㒳")
        self.assertEqual(Operator.Jia.name, "夾")

        self.assertEqual(Operator.Luan.name, "䜌")
        self.assertEqual(Operator.Ban.name, "辦")
        self.assertEqual(Operator.Lin.name, "粦")
        self.assertEqual(Operator.Li.name, "瓥")
        self.assertEqual(Operator.Yi.name, "燚")


if __name__ == "__main__":
    unittest.main()
