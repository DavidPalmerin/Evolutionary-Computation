import math
import random as rnd

class Utils:

	def box_muller_transform(self, sqrd_sigma):
		'''
			Standard Normal Distribution random numbers generator 
			    from uniform random numbers.
			Box-Muller Method implementation.
			http://www.lmpt.univ-tours.fr/~nicolis/Licence_NEW/08-09/boxmuller.pdf
		'''
		p = rnd.uniform(0,1)
		t = rnd.uniform(0,1)
		s = 1 - p
		sigma = math.sqrt(sqrd_sigma)
		z_1 = math.sqrt(-2 * math.log(s)) * math.cos(2 * math.pi * t)
		return float(sigma * z_1)

	def sphere(self, vector, dim):
		'''
			Sphere function.
		'''
		squares = []
		for i in range(dim):
			squares.append(vector[i]**2)
		return sum(squares)
