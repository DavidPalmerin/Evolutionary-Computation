import math
import random as rnd
from Utils import *

class ES1vs1:

	def __init__(self):
		self.utils = Utils()

	def mutate(self, vector, dim):
		child = vector[:]
		sigma = vector[dim]
		for i in range(dim):
			noise = self.utils.box_muller_transform(sigma)
			child[i] += noise
			i += 1
		return child

	def phi(self, num_success, h):
		ratio = num_success / h
		if ratio < 0.2:
			return 0.82
		elif ratio > 0.2:
			return 1.22
		return 1

	def one_fifth_rule(self, vector, dim, num_success, h):
		alpha = self.phi(num_success, h)
		vector[dim] *= alpha 

	def run(self, x_0, dim, F, success=False):
		print("---- Estrategia Evolutiva 1+1 ----")
		precision = 0.001
		h, check = 1, dim * 10
		num_success = 0

		x_i, fx_i = x_0, F(x_0, dim)
		counter = 0
		bound = 10e5
		while abs(fx_i) > precision and counter < bound:
			child = self.mutate(x_i, dim)
			f_child = F(child, dim)
			if abs(f_child) < abs(fx_i):
				x_i = child
				fx_i = f_child
				num_success += 1
			h += 1

			# Cambio de sigma.
			if success and h % check == 0:
				self.one_fifth_rule(x_i, dim, num_success, h)
				num_success = 0
			counter += 1

		print("> Usando regla 1/5: %s" % str(success))
		print("> Número de dimensiones: %d" % dim)
		print("> Número de iteraciones: %d" % counter)
		return x_i



