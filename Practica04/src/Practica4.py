import random as rnd
from GA import *
from visualizador import grafica

def ejercicio_1():
	print("> Ejercicio 1")
	goal = [102, 51, 0, 0, 0, 0, 198, 10]
	total_genomes = 75
	codification = [(0,255)] * 6
	max_its = 75
	codification.extend([(0,300), (1,45)])

	g_a = GA(codification, goal, total_genomes)
	p_0 = g_a.initial_population()
	f = g_a.fitness_function

	f_best, best = g_a.evolve(p_0, max_its, f)

	print("Numero de generaciones: %d" % max_its)
	print("Meta:  %s" % goal)
	print("Final: %s con F(x) = %d" % (best, f_best))

def ejercicio_2():
	print("> Ejercicio 2")
	goal = [1, 21, 180, 95, 1, 1]
	total_genomes = 75
	codification = [(0,1), (1,23), (173,400), (75,400), (0,1), (0,1)]
	max_its = 75

	g_a = GA(codification, goal, total_genomes)
	p_0 = g_a.initial_population()
	f = g_a.fitness_function

	f_best, best = g_a.evolve(p_0, max_its, f)

	print("Numero de generaciones: %d" % max_its)
	print("Meta:  %s" % goal)
	print("Final: %s con F(x) = %d" % (best, f_best))

def ejercicio_3():
	print("> Ejercicio 3")
	goal = [51, 153, 255, 249, 229, 189, 255, 255, 0, 180, 21,3]
	total_genomes = 100
	max_its = 100
	codification = [(0,255)] * 9
	codification.extend([(0, 300), (1,45), (0,4)])

	g_a = GA(codification, goal, total_genomes)
	p_0 = g_a.initial_population()
	f = g_a.fitness_function

	f_best, best = g_a.evolve(p_0, max_its, f)

	print("Numero de generaciones: %d" % max_its)
	print("Meta:  %s" % goal)
	print("Final: %s con F(x) = %d" % (best, f_best))
	print("Ver imagenes meta.png y final.png")

	grafica(goal[0], goal[1], goal[2], goal[3], goal[4], goal[5], goal[6], goal[7], goal[8], "meta.png")
	grafica(best[0], best[1], best[2], best[3], best[4], best[5], best[6], best[7], best[8], "final.png")



print("---- Practica 4 ----")
print("1. Ejercicio 1")
print("2. Ejercicio 2")
print("3. Ejercicio 3")
op = int(input("> Seleccionar "))

if op == 1:
	ejercicio_1()
elif op == 2:
	ejercicio_2()
else:
	ejercicio_3()




