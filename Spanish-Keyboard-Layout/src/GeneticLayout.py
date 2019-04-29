from Layout import *

class GeneticLayout:

    def __init__(self, num_generations=100,
                 population_size=100):
        self.GENERATIONS = num_generations
        self.POPULATION  = population_size
        self.OFFSPRING_BOUND = int(population_size * 0.75)
        self.MTN_PROB = 0.10
        self.RMB_PROB = 0.85

        self.generation = self.random_population()
        self.best = self.best_individual()

    def random_population(self):
        population = []
        for i in range(self.POPULATION):
           layout = Layout()
           population.append(layout)
        return population

    def breed(self):
        offspring = []
        while len(offspring) < self.POPULATION:
            p1, p2 = self.select_parents(rnd_bound=self.POPULATION)
            h1, h2 = self.get_children(p1, p2)
            offspring.append(h1)
            offspring.append(h2)
        return offspring

    def evolve(self):
        counter = 0
        while counter < self.GENERATIONS:
            print("Generation %d..." % counter)
            offspring = self.breed()
            self.population = self.select_new_population(offspring)
            counter += 1
        return self.best_individual()

    def get_children(self, p1, p2):
        child1, child2 = None, None
        if rnd.uniform(0,1) <= self.RMB_PROB:
            child1 = p1.recombine(p2)
            child2 = p2.recombine(p1)
        else:
            child1 = p1.copy()
            child2 = p2.copy()
        self.mutate(child1)
        self.mutate(child2)
        return child1, child2

    def mutate(self, layout):
        for letter1 in layout.alphabet:
            if rnd.uniform(0,1) < self.MTN_PROB:
                i = rnd.randint(0, len(layout.alphabet) - 1)
                letter2 = layout.alphabet[i]
                layout.mutate(letter1, letter2)

    '''
        Próximas funciones son para selección de padres y
        de nueva población.
    '''
    def select_new_population(self, offspring):
        bound = self.OFFSPRING_BOUND
        new_population = self.select_k_population(offspring, bound)

        new_population.append(self.best_individual())

        bound = self.POPULATION - self.OFFSPRING_BOUND - 1
        new_population.extend(self.select_k_population(self.generation, bound))

        return new_population

    def select_k_population(self, population, bound):
        it = 0
        next_population = []
        while it < bound:
            p1, p2 = self.select_parents(bound, population)
            next_population.append(p1)
            if it + 1 < bound:
                next_population.append(p2)
            it += 2
        return next_population

    def select_parents(self, rnd_bound, pool=None):
        k = int(rnd_bound * 0.25)
        if pool == None:
            return self.tournament_selection(self.generation, k, rnd_bound)
        return self.tournament_selection(pool, k, rnd_bound)

    def tournament_selection(self, pool, k, rnd_bound):
        bests = [None, None]
        for i in range(2):
            k_gen = self.select_k_generation(pool, k, rnd_bound)
            bests[i] = min(k_gen)
        return bests[0], bests[1]

    def select_k_generation(self, pool, k, rnd_bound):
        selected = set([])
        while k > 0:
            i = rnd.randint(0, rnd_bound - 1)
            while i in selected:
                i = rnd.randint(0, rnd_bound - 1)
            selected.add(i)
            k -= 1
        return [pool[i] for i in list(selected)]

    def best_individual(self):
        return min(self.generation)


if __name__ == '__main__':
    gl = GeneticLayout()
    pop = gl.random_population()
    best = gl.evolve()
    print(best)

