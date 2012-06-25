#coding: utf-8

def hello():
	'''
		This is a test

		>>> hello()
		hello

	'''
	print 'hello'
def loadit():
	f = open(u'/Users/Arthur/Documents/Test/a.txt', 'r')
	i=0
	for x in f:
		if i<1000:
			x.replace('\r',"").replace('\n',"").replace('\r\n',"")
			r=x.split('#')
			print r[-1]
			print x

if __name__=='__main__':
	#import doctest
	##doctest.testmod()
	loadit()