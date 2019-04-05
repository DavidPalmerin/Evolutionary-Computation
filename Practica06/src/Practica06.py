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
	print("Numero aleatorio: %f" % rnd_num)

def ejercicio_2():
	dim = int(input('Número de dimensiones > '))
	op = input('¿Usar regla 1/5? s/n > ')
	success = True if op == 's' or op == 'S' else False
	es = ES1vs1()
	utils = Utils()
	x_0 = [-99] * dim
	x_0.append(1.0)
	x_f = es.run(x_0, dim, utils.sphere, success)
	print("¡Optimo encontrado!")
	print("~ %s" % str(x_f))
	print("~ F(x_f) = %f" % utils.sphere(x_f, dim))

def ejercicio_3():
	es = ES_mu_lambda()
	utils = Utils()
	dim = int(input('Número de dimensiones > '))
	mu_size = 15
	lambda_size = 130
	x_f = es.run(dim, utils.sphere, mu_size, lambda_size)
	print("F(x_f) = %f" % utils.sphere(x_f, dim))
	
	file = open('out.txt', 'w')
	for v in es.values:
		file.write('%s\n' % str(v))
	file.close()

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



