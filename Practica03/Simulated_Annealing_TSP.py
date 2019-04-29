# -*- coding: utf-8 -*-
'''
    Palmerin Morales David Gabriel.
    Cómputo Evolutivo - Práctica 03 
    Semestre 2019-2
    Programación de Recocido Simulado para aproximaciones
    a soluciones de instancias del problema TSP.

    Se usa Temperatura inicial de 100
    Se usa el sistema de enfriamiento de Kirkpatrick:
        T_k+1 = T_k * alpha
        donde escogí alpha = 0.99.
    
    Los vecinos de un estado s son todas las permutaciones
    de dos elementos del estado s.
      Se experimentó intercambiando dos elementos aleatorios i,j in s[1:15] 
      con i != j. Sin embargo, no obtenía muy buenos resultados.
      La impliementación de vecindad que es muchísimo menos eficiente (en tiempo 
      de ejecución)pero obtiene mejores rutas (en mi implementación) 
      es obtener todas las posibles permutaciones de dos elementos de un estado s. 
      Es decir, en cada iteración calculamos O(n^2) swaps con n=16. Y finalmente, 
      aleatoriamente seleecciona uno de todos los obtenidos.
      Cómo se mencionó anteriormente, esta última aproximación obtuvo mejores 
      rutas en de mi implementación. 

    F es la función de costo.
    P es la función de probabilidad de Boltzmann.
    N es la función de vecindad.

    Se requiere instalar mysql.connector y gmplot.

    La mejor ruta que encontré fue con ORIGEN = 1 y DESTINO = 2
    x_f = [1, 11, 12, 13, 14, 15, 16, 10, 8, 9, 5, 7, 6, 3, 4, 2]
        donde F(x_f) = 11349.229712
    Se anexa screenshot con tal ruta. 
'''

import math
import gmplot
import numpy as np
import random as rnd
import mysql.connector as mysql
import matplotlib.pyplot as plt

mysql_connection = mysql.connect(user='root', password='', database='tsp')
cursor = mysql_connection.cursor()

NORMALIZER = 0
COSTS = []
ITERS = 0
MUSEOS = [  'UNIVERSUM',
            'TEMPLO_MAYOR',
            'ANTIGUO_COLEGIO_DE_SAN_ILDEFONSO',
            'PALACIO_NACIONAL',
            'MUSEO_NACIONAL_DE_ARTE',
            'MUSEO_DEL_ESTANQUILLO',
            'ANTIGUO_PALACIO_DE_ITURBIDE',
            'MUSEO_FRANZ_MAYER',
            'MUSEO_DE_MEMORIA_Y_TOLERANCIA',
            'MUSEO_SOUMAYA',
            'MUSEO_CASA_DEL_RISCO',
            'MUSEO_DE_EL_CARMEN',
            'MUSEO_DE_ARTE_CARRILLO_GIL',
            'MUSEO_CASA_DE_LEON_TROTSKY',
            'MUSEO_DE_HISTORIA_NATURAL',
            'MUSEO_DE_ARTE_MODERNO'
        ]

def edge_weight(origin, dest):
    query = "SELECT distancia FROM conexiones WHERE id_m1=%d AND id_m2=%d" % (origin, dest)
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        dist = result[0]
        return dist[0]
    return fake_weight(origin, dest)

def fake_weight(origin, dest):
    radius = 6373000
    a = A(origin, dest)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c * NORMALIZER

def normalizer():
    query = "SELECT distancia FROM conexiones"
    cursor.execute(query)
    weights = cursor.fetchall()
    weights.sort()
    
    w_sum = 0
    for i in range(len(weights) - 1):
        w_sum += weights[i][0]
    return w_sum

def A(origin, dest):
    (o_lat, o_lon) = get_coordinates(origin)
    (d_lat, d_lon) = get_coordinates(dest)
    left  = math.sin((d_lat - o_lat) / 2) ** 2
    right = math.cos(o_lat) * math.cos(d_lat) * (math.sin((d_lon - o_lon)/2) ** 2)
    return left + right

def F(s):
    size = len(s)
    w_sum = 0
    for i in range(size - 1):
        w_sum += edge_weight(s[i], s[i + 1])

    return w_sum / NORMALIZER

def P(current_f, next_f, T):
    if next_f < current_f:
        return 1
    return math.exp((current_f - next_f) / T)

def N(perm):
    all_perms = perm_pairs(perm[1:-1])
    i = rnd.randint(0, len(all_perms) - 1)
    return perm[:1] + all_perms[i] + perm[-1:]

def perm_pairs(arr):
  perms = []
  for i in range(len(arr)):
    for j in range(i + 1, len(arr)):
      p_m  = arr[:]
      p_m[i] = arr[j]
      p_m[j] = arr[i]
      perms.append(p_m)
  return perms

def simulated_annealing(x_0, f, T_0, epsilon):
    global COSTS
    global ITERS
    
    best_s, best_fs = x_0, f(x_0)
    last_fs = best_fs
    alpha  = 0.99
    k = 0
    while last_fs != best_fs or k == 0: 
        T = T_0
        curr_s, curr_fs = best_s[:], best_fs
        while T > epsilon:
            new_s  = N(curr_s)
            new_fs = f(new_s)
            if P(curr_fs, new_fs, T) >= rnd.uniform(0,1):
                curr_s, curr_fs = new_s[:], new_fs
            else:
                new_s, new_fs = curr_s[:], curr_fs

            if curr_fs < best_fs:
                best_s, best_fs = curr_s[:], curr_fs
                last_fs = best_fs
            COSTS.append(curr_fs)
            T = T * alpha
            k += 1

        if last_fs == best_fs: 
            break
    
    ITERS = k
    return best_s


def seed(origin, dest):
    x_0 = [i + 1 for i in range(16)]
    x_0 = list(np.random.permutation(x_0))

    (i, j) = (-1,-1)
    for k in range(len(x_0)):
        if x_0[k] == origin:
            i = k
        if x_0[k] == dest:
            j = k

    swap(x_0, 0, i)
    swap(x_0, -1, j)
    return x_0


def swap(ls, i, j):
    aux = ls[i]
    ls[i] = ls[j]
    ls[j] = aux

def get_coordinates(m_id):
    query = "SELECT latitud, longitud FROM museos WHERE MuseoId=%d" % m_id
    cursor.execute(query)
    (lat, lon) = cursor.fetchall()[0]
    return (math.radians(lat), math.radians(lon))

def all_coordinates():
    query = "SELECT latitud, longitud FROM museos"
    cursor.execute(query)
    res = cursor.fetchall()
    return res

def match_coordinates(path, coordinates):
    lats  = []
    longs = []
    for i in range(len(coordinates)):
        museo = path[i]
        lats.append(coordinates[museo - 1][0])
        longs.append(coordinates[museo - 1][1])

    return (lats, longs)

def g_plot(lats, longs, file_name):
    gmap = gmplot.GoogleMapPlotter(lats[0], longs[0], 10)
    gmap.plot(lats, longs, 'cornflowerblue', edge_width=2)
    gmap.draw(file_name)

def graph_function(x_range, y_range):
    plt.plot(x_range, y_range)
    plt.show()

if __name__ == '__main__':
    NORMALIZER = normalizer()
    T = 100
    epsilon = 0.01

    print("\n---------- TSP con Recocido Simulado ----------")
    print("---------- Temperatura inicial = 100 ----------")
    print("---------- Enfriamiento con a = 0.99 ----------")
    print("---------- Epsilon definida e = 0.01 ----------\n")

    print("0. Origen y destino default.")
    print("1. Origen y destino elegido por usuario.")
    print("2. Origen y destino aleatorios.")
    op = int(raw_input("\t>")) % 3

    ORIGEN, DESTINO = 1, 2
    if op == 1:
        print("Origen [1, ..., 16]: ")
        ORIGEN = int(raw_input()) 
        print("Destino [1, ..., 16]: ")
        DESTINO = int(raw_input())
        while ORIGEN == DESTINO:
            print("El destino debe ser distinto al origen.")
            print("Destino [1, ..., 16]: ")
            DESTINO = int(raw_input()) % 16
        if ORIGEN == 0 or DESTINO == 0:
            print("El rango es [1,..,16] :(")
            exit(0)

    elif op == 2:
        ORIGEN = rnd.randint(1, 16)
        DESTINO = rnd.randint(1,16)
        while ORIGEN == DESTINO:
          DESTINO = rnd.randint(1,16)
    name_o, name_d = MUSEOS[ORIGEN - 1], MUSEOS[DESTINO - 1]

    single_exec = True
    print("0. Comparar 5 ejecuciones.")
    print("1. Una ejecucion.")
    exe = int(raw_input("\t>"))
    single_exec = False if exe == 0 else True

    x_0 = seed(ORIGEN, DESTINO)
    print("\tx_0 = %s F(x_0) = %d" % (str(x_0), F(x_0)))
    solutions = []
    ev_solutions = []
    best_index = -1
    num_exec = 1 if single_exec else 5
    t = 0
    while t < num_exec:
        print("\n~ Ruta de %s a %s" % (name_o, name_d))

        x_f = simulated_annealing(x_0, F, T, epsilon)
        ev_xf = F(x_f)
        solutions.append(x_f)
        ev_solutions.append(ev_xf)

        print("\tRuta encontrada!")
        print("\tx_f = %s F(x_f) = %f" % (str(x_f), F(x_f)))
        if t == 0 or ev_xf < ev_solutions[best_index]:
            best_index = t
        t += 1

    x_f = solutions[best_index]
    best_f = F(x_f)
    coordinates = all_coordinates()
    (lats, longs) = match_coordinates(x_f, coordinates)
    file_name = "SA_Path.html"
    g_plot(lats, longs, file_name)
    print("\nLa mejor ruta encontrada con peso F(x_f) = %f" % (best_f))
    print("\t%s" % MUSEOS[x_f[0] - 1])
    for i in range(1, len(x_f)):
        print("\t-> %s" % MUSEOS[x_f[i] - 1])
    print("Ver archivo: %s" % file_name)

    if not single_exec:
        print("\nSe grafico la comparacion de costos de cada iteracion.")
        graph_function([i for i in range(num_exec)], ev_solutions)

    if single_exec:
        print("Se grafico Costo vs. Iteracion")
        graph_function([i for i in range(ITERS)], COSTS)

