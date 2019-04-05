import sys
import math
import random as rnd

from Utils import *
from ES1vs1 import *
from ES_mu_lambda import *

def ejercicio_1():
	utils = Utils()
	sigma = 1.0
	rnd_num = utils.box_muller_transform(sigma)
	print("Número aleatorio: %f" % rnd_num)

def ejercicio_2():
	dim = int(input('Número de dimensiones > '))
	op = input('¿Usar regla 1/5? s/n > ')
	success = True if op == 's' or op == 'S' else False
	es = ES1vs1()
	utils = Utils()
	x_0 = [-99] * dim
	x_0.append(1.0)
	x_f = es.run(x_0, dim, utils.sphere, success)

	print("> x_f = %s" % str(x_f))
	print("> F(x_f) = %f" % utils.sphere(x_f, dim))
    
def ejercicio_3():
	es = ES_mu_lambda()
	utils = Utils()

	print("Seleccionar función:")
	fun_op = int(input('1. Sphere \n2. Ackley \n > '))
	dim = int(input('Número de dimensiones > '))
	fun = utils.sphere if fun_op == 1 else utils.ackley

	if dim == 2:
		bound = 5 if fun_op == 1 else 1
		interval = np.linspace(-bound, bound)
		utils.graph_contours(fun, interval, interval)

	mu_size = 14
	lambda_size = 100
	x_f = es.run(dim, fun, mu_size, lambda_size)
	
	print("> x_f = %s" % str(x_f))
	print("> F(x_f) = %f" % fun(x_f, dim))	

if __name__ == '__main__':
	if len(sys.argv) > 1:
		op = int(sys.argv[1])
		if op == 1:
			ejercicio_1()
		elif op == 2:
			ejercicio_2()
		else:
			ejercicio_3()
	else:
		print("Usar: python3 Practica06.py [1,2 o 3]")



