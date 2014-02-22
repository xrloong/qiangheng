# coding=utf8

class Shape:
    pass

class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def setGeometry(self, x, y, w, h):
        [self.x, self.y, self.w, self.h,]=[x, y, w, h,]

    def getGeometry(self):
        return [self.x, self.y, self.w, self.h,]

    def __str__(self):
        return "(%s, %s, %s, %s)"%(self.x, self.y, self.w, self.h,)

