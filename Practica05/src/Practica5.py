from GA import *
import sys
import schematax
import matplotlib.pyplot as plt

def fitness_fun(bits):
	return sum(bits)

def stats_e2(iters, g_a, p_0):
	x_axis = [i for i in range(iters)]
	y_axis = []
	(f_best, best) = (-1,-1)
	for i in range(iters):
		print("\t> Ejecución %d" % i)
		(f_sol, sol) = g_a.evolve(p_0, max_its=100, cost_fun=fitness_fun)
		y_axis.append(f_sol)
		
		if f_sol > f_best or i == 0:
			f_best = f_sol
			best = sol
	
	str_best = ''.join([str(b) for b in best])
	print("\n~ Mejor solución encontrada: ")
	print("\t X = %s \n\t F(X) = %d" % (str_best, f_best))
	
	gen_metrics = g_a.GENERATIONS_AVG
	x_range = [i+1 for i in range(100)]
	plt.plot(x_range, [e for (e,v) in gen_metrics], '-b', label='Óptimo')
	plt.plot(x_range, [v for (e,v) in gen_metrics], '-r', label='Promedio')
	plt.legend(loc='lower right')
	plt.xlabel("Generaciones")
	plt.ylabel("Fitness")
	plt.show()

def ejercicio_2():
	print("~ Ejercicio 2")
	genome_size = 30
	codification = [(0,1)] * genome_size
	g_a = GA(codification, pop_size=100, mtn_prob=0.01, rmb_prob=0.7)
	p_0 = g_a.initial_population()
	simulaciones = 20
	stats_e2(simulaciones, g_a, p_0)

def ejercicio_3():
	print("~ Ejericio 3A")
	genome_size = 10
	codification = [(0,1)] * genome_size

	pop_size = 30
	max_its  = 100
	g_a = GA(codification, pop_size=pop_size, mtn_prob=0.01, rmb_prob=0.7)
	p_0 = g_a.initial_population()
	(f_best, best) = g_a.evolve(p_0, max_its=max_its, cost_fun=fitness_fun)
	print("Best: %s" % best)

	ejercicio_3B(g_a, max_its, pop_size)
	ejercicio_3C(g_a)
	

def ejercicio_3B(g_a, max_its, pop_size):
	print("~ Ejercicio 3B")
	(blocks, top_schemas) = g_a.schemas_metrics()
	x_range = [i + 1 for i in range(max_its)]
	o_range = []
	l_range = []
	for (ls, o_s, l_s) in blocks:
		o_range.append(o_s / pop_size)
		l_range.append(l_s / pop_size)
	plt.plot(x_range, o_range, '-b', label='Orden Promedio')
	plt.plot(x_range, l_range, '-r', label='Longitud Promedio')
	plt.legend(loc='upper right')
	plt.xlabel("Generaciones")
	plt.ylabel("Scale")
	plt.show()

def ejercicio_3C(g_a):
	# Histograma de frecuencias.
	print("~ Ejercicio 3C\n\t Ver gráfica")
	bloques = list(g_a.BLOCKS.values())
	x_range = [i + 1 for i in range(min(bloques), max(bloques))]	
	plt.hist(bloques, bins=x_range, rwidth=0.95, facecolor='blue', alpha=0.5)
	plt.ylabel("# Bloques Constructores")
	plt.xlabel("Repeticiones")
	plt.show()

	bloques = [(g_a.BLOCKS[k], k) for k in g_a.BLOCKS]
	bloques.sort()
	print("~ Ejercicio 3D.\n\tTop 10 Bloques Constructores")
	for e in bloques[-10:]:
		print("\t Bloque constructor: %s con %d repeticiones" % (e[1], e[0]))

if len(sys.argv) > 1:
	op = int(sys.argv[1])
	if op == 2:
		ejercicio_2()
	else:
		ejercicio_3()
else:
	print("Uso: python3 Practica5.py [2 o 3]")

