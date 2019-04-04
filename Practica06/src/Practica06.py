import math
import random as rnd
from Utils import *
from ES1vs1 import *
from ES_mu_lambda import *

def ejercicio_1():
	utils = Utils()
	sigma = 1.0
	rnd_num = utils.box_muller_transform(sigma)
	print(rnd_num)



es = ES1vs1()
utils = Utils()
dim = 100
x_0 = [-99] * dim
x_0.extend([1.0] * dim)
x_f = es.run(x_0, dim, utils.sphere, success=True)
print("F(x_f) = %f" % utils.sphere(x_f, dim))
ejercicio_1()

# dim = 10
# es = ES_mu_lambda()
# x_f = es.run(dim, utils.sphere, 10, 100)
# print("F(x_f) = %f" % utils.sphere(x_f, dim))


