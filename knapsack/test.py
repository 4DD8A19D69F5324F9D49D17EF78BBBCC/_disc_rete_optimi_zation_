def a():
	x=1
	def b(y):
		print x+y
		x=12
	b(11)
a()	
