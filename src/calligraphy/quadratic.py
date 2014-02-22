import math

def solveMin(s0, s1, s2):
	a=s0-2*s1+s2
	b=2*(s1-s0)
	c=s0

	if a>0:
		# it happends at t=-b/(2*a)
		t=-b/(2*a)
		if 0<=t<=1:
			tmpMinX=(1-t)*(1-t)*s0 + 2*(1-t)*t*s1 + t*t*s2
			return math.floor(tmpMinX)
	return min(s0, s2)

def solveMax(s0, s1, s2):
	a=s0-2*s1+s2
	b=2*(s1-s0)
	c=s0

	if a<0:
		# it happends at t=-b/(2*a)
		t=-b/(2*a)
		if 0<=t<=1:
			tmpMinX=(1-t)*(1-t)*s0 + 2*(1-t)*t*s1 + t*t*s2
			return math.ceil(tmpMinX)
	return max(s0, s2)


