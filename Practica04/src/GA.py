import random as rnd

class GA:

	MTN_PROB = 0.10
	RMB_PROB = 0.75

	def __init__(self, codification, goal, pop_size):
		'''
			codification: Indica el rango de cada entrada del genoma.
				Por ejemplo, si tenemos un genemoa que representa un color rgb
				entonces un genom válido es [2, 234, 211]. En este caso,
				la codificacion es [(0,255), (0,255), (0,255)]. Esto es util
				para la mutacion, asi sabemos que valores son válidos.
			goal: Genoma meta al que queremos llegar.
			pop_size: Tamaño de la poblacion de cada generacion.
		'''
		self.codification = codification
		self.GOAL = goal
		self.TOTAL_GENOMES = pop_size
		self.GENOME_LENGTH = len(goal)
		self.OFFSPRING_BOUND = int(pop_size * 0.75)

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
		(l,r) = self.get_crosspoints()
		g1_substr = genome_1[l:r]
		genome_1[l:r] = genome_2[l:r]
		genome_2[l:r] = g1_substr
		return genome_1, genome_2

	def get_crosspoints(self):
		'''
			Obtiene dos puntos aleatorios dentro del rango de un genoma.
			Estos puntos se usan en la operador de recombinacion
			El resultado es una tupla (p1, p2) donde p1 < p2
		'''
		pivot_1 = rnd.randint(0, self.GENOME_LENGTH - 2)
		pivot_2 = rnd.randint(0, self.GENOME_LENGTH - 1)
		while pivot_2 == pivot_1 or abs(pivot_1 - pivot_2) == self.GENOME_LENGTH - 1:
			pivot_2 = rnd.randint(0, self.GENOME_LENGTH - 1)
		return (pivot_1, pivot_2) if pivot_1 < pivot_2 else (pivot_2, pivot_1)

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
		print("\tEvolucionando...")
		p_i = initial_population
		while max_its > 0:
			children_counter = 0
			new_generation = []
			# roulette = self.roulette_probability(cost_fun, p_i)
			f_pi, total = self.population_fitness(cost_fun, p_i)

			while children_counter < self.OFFSPRING_BOUND + 1:
				# parent_1, parent_2 = self.choose_parents(roulette)
				parent_1, parent_2 = self.choose_parents_tournament(p_i, cost_fun, self.TOTAL_GENOMES)
				child_1, child_2 = self.create_children(parent_1[:], parent_2[:])

				if rnd.uniform(0,1) < 0.8:
					child_1 = self.mutation(child_1)
					child_2 = self.mutation(child_2)

				new_generation.append(child_1)
				new_generation.append(child_2)
				children_counter += 2
			# p_i = self.new_population(p_i, new_generation, cost_fun)
			p_i = self.next_generation(p_i, new_generation, cost_fun)
			max_its -= 1

		fitness_pi, total_sum = self.population_fitness(cost_fun, p_i)
		return min(fitness_pi)

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
		Implementacion con seleccion por torneo.
		https://en.wikipedia.org/wiki/Tournament_selection
		Selecciona los papás y los miembros de la nueva poblacion
		con esta tecnia.
	'''
	def next_generation(self, parents, offspring, F):
		'''
			Obtiene la nueva generacion de individuos.
			parents: Es la poblacion padre.
			offspring: Poblacion creada durante la iteracion de evolve.
			F: funcion fitness a usar.
			Obtiene una nueva poblacion de tamaño self.TOTAL_GENOMES.
			La nueva poblacion se conforma por una una cantidad 
			de self.OFFSPRING_BOUND individuos y el resto por individuos
			de la generacion padre.
			Estos elementos son elegidos aleatoriamente.
			Siempre se agrega el mejor individuo de la poblacion padre a la 
			nueva poblacion.
		'''
		new_population = []
		bound = self.OFFSPRING_BOUND
		self.choose_next_generation(new_population, offspring, bound, F)

		# Se queda con el mejor de la generacion anterior.
		f_population = [(F(g), g) for g in parents]
		new_population.append(min(f_population)[1])


		bound = self.TOTAL_GENOMES - self.OFFSPRING_BOUND - 1
		self.choose_next_generation(new_population, parents, bound, F)

		return new_population

	def choose_next_generation(self, next_population, population, bound, F):
		'''
			Añade una cantidad bound de individuos a la lista next_population.
			next_population: lista donde se guardan los nuevos genomas.
			population: lista de donde seleccionaremos los genomas que estarán
			            en la nueva generacion.
			bound: Cantidad de genomas que queremos guardar.
			F: Funcion fitness a usar.
		'''
		it = 0
		while it < bound:
			p_1, p_2 = self.choose_parents_tournament(population, F, bound)
			next_population.append(p_1)
			if it + 1 < bound:
				next_population.append(p_2)
			it += 2

	def choose_parents_tournament(self, population, F, rnd_bound):
		'''
			Seleccion por torneos.
			population: Poblacion de donde seleccionaremos los dos padres.
			F: Funcion que evalua a los genomas.
			rnd_bnd: Cota para elegir el numero de elementos a escoger.
			La seleccion por torneos requiere de escoger k elementos
			y de ellos obtener el que tenga mejor fitness.
			https://en.wikipedia.org/wiki/Tournament_selection
		'''
		k = int(rnd_bound * 0.25)
		return self.tournament_selection(population, k, F, rnd_bound)

	def tournament_selection(self, population, k, F, rnd_bound):
		'''
			Seleccion por torneos. 
			https://en.wikipedia.org/wiki/Tournament_selection
			population: Poblacion de donde escogeremos los individuos.
			k: Numero de individuos que tomaremos de acuerdo a esta tecnica.
			F: Funcion fitness para genomas.
			rnd_bound: Cota para escoger elementos.
		'''
		bests = [0,0]
		for i in range(2):
			k_pop = self.select_k_population(population, k, F, rnd_bound)
			bests[i] = min(k_pop)
		return bests[0][1], bests[1][1]

	def select_k_population(self, population, k, F, rnd_bound):
		'''
			Selecciona k elementos aleatorios de una poblacion.
			population: Poblacion de donde tomaremos los individuos.
			k: Numero de individuos a tomar.
			F: Funcion fitness para genomas.
			rnd_bnd: Cota para elegir elementos.
		'''
		indices = []
		while k > 0:
			index = rnd.randint(0, rnd_bound - 1)
			while index in indices:
				index = rnd.randint(0, rnd_bound - 1)
			indices.append(index) 
			k -= 1
		f_population, total = self.population_fitness(F, population)
		return [f_population[i] for i in indices]

	'''
		Implementacion con ruleta.
		Selecciona papás y nueva poblacion por medio de ruleta.
	'''
	# def select_population(self, new_population, roulette, bound):
	# 	it = 0
	# 	while it < bound:
	# 		(h_1, h_2) = self.choose_parents(roulette)
	# 		new_population.append(h_1)
	# 		if it + 1 < bound:
	# 			new_population.append(h_2)
	# 		it += 2

	# def new_population(self, parents, offspring, F):
	# 	roulette = self.roulette_probability(F, offspring)
	# 	next_population = []
	# 	self.select_population(next_population, roulette, self.OFFSPRING_BOUND)	
	# 	# Se queda con el mejor de la generacion anterior.
	# 	f_population = [(F(g), g) for g in parents]
	# 	next_population.append(max(f_population)[1])

	# 	roulette = self.roulette_probability(F, parents)
	# 	bound = self.TOTAL_GENOMES - self.OFFSPRING_BOUND - 1
	# 	self.select_population(next_population, roulette, bound)

	# 	return next_population

	# def choose_parents(self, roulette):
	# 	parents = [0,0]
	# 	for i in range(2):
	# 		rnd_num = rnd.uniform(0,1)
	# 		for (scope, gen) in roulette:
	# 			if rnd_num < scope:
	# 				parents[i] = gen
	# 				break
	# 	return parents

	# def population_probabilities(self, F, population):
	# 	fitness, total_sum = self.population_fitness(F, population)
	# 	return [(v / total_sum, g) for (v,g) in fitness]

	# def roulette_probability(self, F, population):
	# 	fitness = self.population_probabilities(F, population)
	# 	acc = fitness[0][0]
	# 	roulette = [(fitness[0][0], fitness[0][1])]
	# 	for i in range(1, len(fitness)):
	# 		(f_gen, gen) = fitness[i]
	# 		acc += f_gen
	# 		roulette.append((acc, gen))
	# 	return roulette
