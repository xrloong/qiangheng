class Operator:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return self.__name

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self.__name

    @staticmethod
    def generateBuiltin(operatorName):
        return Operator(operatorName)


# 龜
# 爲
# 龍雀
# 蚕鴻回
# 起廖載斗
# 同函區左
# 衍衷瓥粦
# 錯

Operator.Turtle = Operator.generateBuiltin("龜")
Operator.Loong = Operator.generateBuiltin("龍")
Operator.Sparrow = Operator.generateBuiltin("雀")
Operator.Equal = Operator.generateBuiltin("爲")

Operator.Silkworm = Operator.generateBuiltin("蚕")
Operator.Goose = Operator.generateBuiltin("鴻")
Operator.Loop = Operator.generateBuiltin("回")

Operator.Qi = Operator.generateBuiltin("起")
Operator.Zhe = Operator.generateBuiltin("這")
Operator.Liao = Operator.generateBuiltin("廖")
Operator.Zai = Operator.generateBuiltin("載")
Operator.Dou = Operator.generateBuiltin("斗")

Operator.Tong = Operator.generateBuiltin("同")
Operator.Han = Operator.generateBuiltin("函")
Operator.Qu = Operator.generateBuiltin("區")
Operator.Left = Operator.generateBuiltin("左")

Operator.Mu = Operator.generateBuiltin("畞")
Operator.Zuo = Operator.generateBuiltin("㘴")
Operator.You = Operator.generateBuiltin("幽")
Operator.Liang = Operator.generateBuiltin("㒳")
Operator.Jia = Operator.generateBuiltin("夾")

Operator.Luan = Operator.generateBuiltin("䜌")
Operator.Ban = Operator.generateBuiltin("辦")
Operator.Lin = Operator.generateBuiltin("粦")
Operator.Li = Operator.generateBuiltin("瓥")
Operator.Yi = Operator.generateBuiltin("燚")
