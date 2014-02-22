from .IM import IM
from character import ARCharInfo

class Array(IM):
	"行列輸入法"

	def __init__(self):
		self.keyMaps=[
			['a', '1-',],
			['b', '5v',],
			['c', '3v',],
			['d', '3-',],
			['e', '3^',],
			['f', '4-',],
			['g', '5-',],
			['h', '6-',],
			['i', '8^',],
			['j', '7-',],
			['k', '8-',],
			['l', '9-',],
			['m', '7v',],
			['n', '6v',],
			['o', '9^',],
			['p', '0^',],
			['q', '1^',],
			['r', '4^',],
			['s', '2-',],
			['t', '5^',],
			['u', '7^',],
			['v', '4v',],
			['w', '2^',],
			['x', '2v',],
			['y', '6^',],
			['z', '1v',],
			['.', '9v',],
			['/', '0v',],
			[';', '0-',],
			[',', '8v',],
			]
		self.nameDict={
				'cn':'行列',
				'tw':'行列',
				'hk':'行列',
				'en':'Array',
				}
		self.iconfile="qhar.svg"
		self.maxkeylength=4

IMInfo=Array
CharInfoGenerator=ARCharInfo.ARCharInfo

if __name__=='__main__':
	pass

