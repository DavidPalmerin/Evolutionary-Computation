import operator
import random as rnd
from Utils import *

class ES_mu_lambda:

	def __init__(self):
		self.utils = Utils()
		self.values = []

	def init_population(self, size, dim, lb, ub):
		population = []
		sigma = 1.0
		while size > 0:
			vector = []
			for i in range(dim):
				val = rnd.randint(lb, ub)
				vector.append(val)
			vector.append(sigma)
			population.append(vector)
			size -= 1
		return population

	def sigma_mutation(self, vector, dim):
		tau_0 = 1.0 / 2 * dim
		tau_i = 1.0 / (2 * math.sqrt(dim))
		z_0 = self.utils.box_muller_transform(1.0)
		z_i = self.utils.box_muller_transform(1.0)
		e = math.exp(tau_i*z_i + z_0*tau_0)
		vector[dim] *= e

	def mutate(self, vector, dim):
		sigma = vector[dim]
		for i in range(dim):
			vector[i] +=  self.utils.box_muller_transform(sigma)
		self.sigma_mutation(vector, dim)

	def get_offspring(self, parents, dim, F, offspring_size):
		n = len(parents)
		offspring = []
		for i in range(offspring_size):
			index = rnd.randint(0,n-1) if i >= n else i
			child = parents[index][:]
			self.mutate(child, dim)
			offspring.append(child)
		return offspring

	def new_mu(self, population, size, F, dim):
		new_population = []
		best = []

		specs = [(F(x, dim), x) for x in population]
		counter = 0
		while counter < size:
			i, (f_x, x) = min(enumerate(specs), key=operator.itemgetter(1))
			new_population.append(x)
			del specs[i]
			if counter == 0:
				best = x
			counter += 1
		return new_population, best

	def population_min(self, population, F, dim):
		specs = [(F(x, dim), x) for x in population]
		return min(specs)

	def run(self, dim, F, mu_size, lambda_size):
		print("\nEstrategia Evolutiva mu-lambda")
		precision = 0.001
		_mu = self.init_population(mu_size, dim, -30, 30)
		_lambda = []

		fx_i, x_i = self.population_min(_mu, F, dim)
		counter = 0
		bound = 10e5
		print("\t Buscando óptimo...")
		while abs(fx_i) > precision and counter < bound:
			_lambda = self.get_offspring(_mu, dim, F, lambda_size)
			_mu, x_i = self.new_mu(_mu + _lambda, mu_size, F, dim)
			fx_i = F(x_i, dim)
			counter += 1

		print("> Mu = %d : Lambda = %d" % (mu_size, lambda_size))
		print("> Número de dimensiones: %d" % dim)
		print("> Número de iteraciones: %d" % counter)
		return x_i




