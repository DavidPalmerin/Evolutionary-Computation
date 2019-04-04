import operator
import random as rnd
from Utils import *

class ES_mu_lambda:

	def __init__(self):
		self.utils = Utils()

	def init_population(self, size, dim):
		population = []
		sigma = 1.0
		while size > 0:
			vector = []
			for i in range(dim):
				val = rnd.randint(-30, 30)
				vector.append(val)
			vector.append(sigma)
			population.append(vector)
			size -= 1
		return population

	def select_parents(self, population):
		n = len(population)
		i_1 = rnd.randint(0, n - 1)
		i_2 = rnd.randint(0, n - 1)
		while i_1 == i_2:
			i_2 = rnd.randint(0, n - 1)
		return population[i_1], population[i_2]

	def recombine(self, p_1, p_2, dim):
		alpha = rnd.uniform(0,1)
		child = []
		for i in range(dim):
			val = p_1[i] + alpha * (p_2[i] - p_1[i])
			child.append(val)

		child.extend(p_1[dim:])
		return child

	def sigma_mutation(self, vector, dim):
		tau_0 = 1.0 / math.sqrt(2 * dim)
		tau_i = 1.0 / dim
		z_0 = self.utils.box_muller_transform(tau_0)
		z_i = self.utils.box_muller_transform(tau_i)
		e = math.exp(z_i + z_0)
		vector[dim] *= e

	def mutate(self, vector, dim):
		self.sigma_mutation(vector, dim)
		noise = vector[dim]
		for i in range(dim):
			vector[i] += noise

	def get_offspring(self, parents, dim, F, offspring_size):
		offspring = []
		while offspring_size > 0:
			p_1, p_2 = self.select_parents(parents)
			child = self.recombine(p_1, p_2, dim)
			offspring.append(child)
			offspring_size -= 1
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
		print("Estrategia Evolutiva mu-lambda")
		precision = 0.001
		_mu = self.init_population(mu_size, dim)
		_lambda = []

		fx_i, x_i = self.population_min(_mu, F, dim)
		while abs(fx_i) > precision:
			print("F(x_i) = %f" % fx_i)
			_lambda = self.get_offspring(_mu, dim, F, lambda_size)
			for p in _lambda:
				self.mutate(p, dim)
			_mu, x_i = self.new_mu(_lambda + _mu, mu_size, F, dim)
			fx_i = F(x_i, dim)
		
		return x_i




