import math
import numpy as np
import random as rnd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

	def ackley(self, vector, dim):
		f_sphere = self.sphere(vector, dim)
		cos_xi = sum([np.cos(2 * np.pi * x_i) for x_i in vector[:dim]])
		c = 1.0 / dim
		return  (-20 * 
			    np.exp(
			    		-0.2 * 
			    		np.sqrt(c * f_sphere) -
			    		np.exp(c * cos_xi)
			    		) +
			    20 + np.exp(1))

	def graph_contours(self, F, x_range, y_range, points=None):
		X,Y     = np.meshgrid(x_range, y_range)
		Z       = F([X,Y], 2)
		levels  = [2 * i for i in range(1, 11)]

		plt.contour(X, Y, Z, levels=levels, colors='grey', linewidths=.5)
		plt.contourf(X, Y, Z)
		if points != None:
			it_array = np.array(points)
			plt.plot(it_array.T[0], it_array.T[1], "x-")
		plt.show()

