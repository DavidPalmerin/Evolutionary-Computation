import random as rnd
import schematax as sx

class GA:

	def __init__(self, codification, pop_size, mtn_prob, rmb_prob):
		'''
			codification: Indica el rango de cada entrada del genoma.
				Por ejemplo, si tenemos un genemoa que representa un color rgb
				entonces un genom válido es [2, 234, 211]. En este caso,
				la codificacion es [(0,255), (0,255), (0,255)]. Esto es util
				para la mutacion, asi sabemos que valores son válidos.
			goal: Genoma meta al que queremos llegar.
			pop_size: Tamaño de la poblacion de cada generacion.
			mtn_prob: Probabilidad de mutación para un gen.
			rmb_prob: Probabilidad de recombinación.
		'''
		self.codification = codification
		self.TOTAL_GENOMES = pop_size
		self.GENOME_LENGTH = len(codification)
		self.OFFSPRING_BOUND = int(pop_size * 0.75)
		self.MTN_PROB = mtn_prob
		self.RMB_PROB = rmb_prob
		self.GENERATIONS = []
		self.GENERATIONS_AVG = []
		self.BLOCKS  = {}

	def fitness_function(self, genome):
		'''
			genome: Genoma del que queremos obtener su fitness.
		'''
		squares = [(self.GOAL[i] - genome[i])**2 for i in range(self.GENOME_LENGTH)]
		return sum(squares)

	def initial_population(self):
		'''
			Obtiene una poblacion inicial aleatoria.
			El tamaño de la poblacion es de tamaño self.TOTAL_GENOMES
			indicado por el usuario.
		'''
		population = []
		it = 0
		while it < self.TOTAL_GENOMES:
			genome = []
			for i in range(self.GENOME_LENGTH):
				(lb, ub) = self.codification[i]
				gen = rnd.randint(lb, ub)
				genome.append(gen)
			population.append(genome)
			it += 1
		return population

	def recombine(self, genome_1, genome_2):
		'''
			Recombina dos genomas.
			Hace cruza con dos puntos aleatorios.
			Regresa dos hijos que son resultado de la combinacion.
		'''
		pivot = rnd.randint(0, self.GENOME_LENGTH - 1)
		g1_init = genome_1[:pivot]
		g2_init = genome_2[:pivot]
		genome_1[:pivot] = g2_init
		genome_2[:pivot] = g1_init

		return genome_1, genome_2

	def mutation(self, genome):
		'''
			Realiza la mutacion de un genoma.
			Cada gen del genoma será alterado con una probabilidad self.MTN_PROB.
			Aqui se usa la codificacion dada en el constructor para saber
			el rango válido para cada entrada en el genoma.
		'''
		for i in range(self.GENOME_LENGTH):
			random_num = rnd.uniform(0,1)
			if random_num < self.MTN_PROB:
				(lb, ub) = self.codification[i]
				genome[i] = rnd.randint(lb, ub)
		return genome

	def create_children(self, parent_1, parent_2):
		'''
			Crea dos hijos a partir de dos padres dados.
			Con probabilidad RMB_PROB los padres se combinaran
			creando los dos hijos.
			Si esto no sucede, entonces regresa copias de los padres.
		'''
		child_1, child_2 = [], []
		rnd_num = rnd.uniform(0,1)
		if rnd_num < self.RMB_PROB:
			child_1, child_2 = self.recombine(parent_1, parent_2)
		else:
			child_1, child_2 = parent_1, parent_2

		return child_1, child_2

	def evolve(self, initial_population, max_its, cost_fun):
		'''
			Funcion principal del algoritmo genetico.
			Realiza el proceso de evolucion de la poblacion.
			initial_population: Poblacion inicial para el algoritmo.
			max_its: Numero de generaciones que se crearán.
			cost_fun: Funcion fitness a usar.
			Regresa el mejor individuo de las iteraciones.
		'''
		print("\t\tEvolucionando...")
		p_i = initial_population
		self.GENERATIONS_AVG = []
		while max_its > 0:
			children_counter = 0
			new_generation = []
			roulette = self.roulette_probability(cost_fun, p_i)
			f_pi, total = self.population_fitness(cost_fun, p_i)
			
			# Metrics.
			self.GENERATIONS_AVG.append((max(f_pi)[0], total/self.TOTAL_GENOMES))
			self.GENERATIONS.append(p_i)

			while children_counter < self.OFFSPRING_BOUND + 1:
				parent_1, parent_2 = self.choose_parents(roulette)
				child_1, child_2 = self.create_children(parent_1[:], parent_2[:])

				if rnd.uniform(0,1) < 0.8:
					child_1 = self.mutation(child_1)
					child_2 = self.mutation(child_2)

				new_generation.append(child_1)
				new_generation.append(child_2)
				children_counter += 2
			p_i = self.next_generation(p_i, new_generation, cost_fun)
			max_its -= 1

		fitness_pi, total_sum = self.population_fitness(cost_fun, p_i)
		return max(fitness_pi)

	def population_fitness(self, F, population):
		'''
			Obtiene una lista de tuplas.
			Cada tupla contiene (f_g, g) donde f_g es el fitness 
			del genoma g.
			population: poblacion de la cual obtendremos la lista de tuplas.
		'''
		total_sum = 0.0
		fitness = []
		for g in population:
			f_g = F(g)
			fitness.append((f_g, g))
			total_sum += f_g
		return fitness, total_sum

	'''
		Implementacion con ruleta.
		Selecciona papás y nueva poblacion por medio de ruleta.
	'''
	def select_population(self, new_population, roulette, bound):
		it = 0
		while it < bound:
			(h_1, h_2) = self.choose_parents(roulette)
			new_population.append(h_1)
			if it + 1 < bound:
				new_population.append(h_2)
			it += 2

	def next_generation(self, parents, offspring, F):
		roulette = self.roulette_probability(F, offspring)
		next_population = []
		self.select_population(next_population, roulette, self.OFFSPRING_BOUND)	

		f_population = [(F(g), g) for g in parents]
		next_population.append(max(f_population)[1])

		roulette = self.roulette_probability(F, parents)
		bound = self.TOTAL_GENOMES - self.OFFSPRING_BOUND - 1
		self.select_population(next_population, roulette, bound)

		return next_population

	def choose_parents(self, roulette):
		parents = [0,0]
		for i in range(2):
			rnd_num = rnd.uniform(0,1)
			for (scope, gen) in roulette:
				if rnd_num < scope:
					parents[i] = gen
					break
		return parents

	def population_probabilities(self, F, population):
		fitness, total_sum = self.population_fitness(F, population)
		return [(v / total_sum, g) for (v,g) in fitness]

	def roulette_probability(self, F, population):
		fitness = self.population_probabilities(F, population)
		acc = fitness[0][0]
		roulette = [(fitness[0][0], fitness[0][1])]
		for i in range(1, len(fitness)):
			(f_gen, gen) = fitness[i]
			acc += f_gen
			roulette.append((acc, gen))
		return roulette

	def schemas_metrics(self):
		blocks = []
		top_schemas = []
		for generation in self.GENERATIONS:
			print("\t> Nueva Generación")
			gen_blocks  = []
			for string in generation:
				s_str = ''.join([str(b) for b in string])
				sx_schema = sx.schema(s_str)
				order = sx_schema.get_order()
				length = sx_schema.get_defining_length()
				gen_blocks.append(s_str)
			top_gen, o_s, l_s = self.top_schemas(gen_blocks)
			top_schemas.append(top_gen)
			blocks.append((gen_blocks, o_s, l_s))

		return (blocks, top_schemas)

	def top_schemas(self, schemas):
		print("\t\tCalculando Bloques Constructores...")
		lattice = sx.complete(schemas)
		print("\t\tBloques Constructores listos.")
		order_sum  = 0.0
		length_sum = 0.0
		for sch in lattice:
			str_sch = str(sch)
			if '*' in str_sch:
				if str_sch in self.BLOCKS:
					self.BLOCKS[str_sch] += 1
				else:
					self.BLOCKS.update({str_sch : 1})
				order_sum += sch.get_order()
				length_sum += sch.get_defining_length()

		schemas = []
		for k in self.BLOCKS.keys():
			v = self.BLOCKS[k]
			schemas.append((v, k))

		# print("> Top 10 bloques constructores:")
		best_schemas = []
		top = 10
		while top > 0 and len(schemas) > 0:
			max_i = 0
			for i in range(len(schemas)):
				if schemas[max_i][0] < schemas[i][0]:
					max_i = i
			elem = schemas[max_i]
			best_schemas.append(elem)
			# print("\t> %s con %d frecuencias" % (elem[1], elem[0]))
			del schemas[max_i]
			top -= 1


		return best_schemas, order_sum, length_sum


