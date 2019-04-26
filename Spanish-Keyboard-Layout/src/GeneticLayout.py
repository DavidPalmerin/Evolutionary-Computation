from Layout import *

class GeneticLayout:

    def __init__(self, fitness_fun,
                 num_generations=100,
                 population_size=100):
        self.F = fitness_fun
        self.GENERATIONS = num_generations
        self.POPULATION  = population_size
        self.MTN_PROB = 0.10
        self.RMB_PROB = 0.85
        self.population = self.random_population()
        self.best = self.best_individual()

    def random_population(self):
        population = []
        for i in range(self.POPULATION):
           layout = Layout()
           layout.set_fitness(rnd.randint(0,500))
           layout.random_layout()
           population.append(layout)
        return population

    def select_parents(self):
        i = rnd.randint(0, self.POPULATION - 1)
        j = rnd.randint(0, self.POPULATION - 1)
        return self.population[i], self.population[j]

    def get_offspring(self):
        offspring = []
        while len(offspring) < self.POPULATION:
            p1, p2 = self.select_parents()
            h1, h2 = self.get_children()

    def evolve(self):
        counter = 0
        while counter < self.GENERATIONS:

            counter += 1

    def get_children(self, p1, p2):
        child = None
        if rnd.uniform() < self.RMB_PROB:
            child = self.recombine(p1.copy(), p2.copy())
        else:
            if rnd.uniform() < 0.5:
                child = p1.copy()
            else: child = p2.copy()
        self.mutate(child)

    def recombine(self, p1, p2):
        bias = 0.5
        child = Layout()
        for l in alphabet:
            [h1,r1,c1] = p1.coordinates[l]
            [h2,r2,c2] = p2.coordinates[l]
            # if child_design[r1][c1]

    def mutate(self, layout):
        print("Not ready")

    def best_individual(self):
        return min(self.population)


if __name__ == '__main__':
    gl = GeneticLayout(lambda x : x)
    pop = gl.random_population()
    best = gl.best_individual()
    print(best)
    print(best.fitness)





