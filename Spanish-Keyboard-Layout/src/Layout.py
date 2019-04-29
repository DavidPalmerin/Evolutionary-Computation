import sys
import random as rnd
from Utils import *

class Layout:

    def __init__(self,
                 coordinates={},
                 design=utils_empty_design(10,3),
                 alphabet=spanish_alphabet(),
                 monograms_file='data/spanish-monograms',
                 bigrams_file='data/spanish-bigrams'):
        self.rows = 3
        self.cols = 10
        self.alphabet = alphabet
        if not coordinates:
            self.coordinates = self.random_layout()
        else: self.coordinates = coordinates
        self.design = self.__to_array__()
        self.monograms = utils_load_ngrams(monograms_file)
        self.bigrams = utils_load_ngrams(bigrams_file)
        self.load_distribution = utils_load_distribution()
        self.coefficients = utils_weight_coefficients()
        self.fitness = self.eval()

    def eval(self):
        load = self.__load_distribution__()
        key = 1.0
        hand = self.__hand_alternation__()
        finger = self.__same_finger_and_hand__()
        steps = self.__no_big_steps__()
        v_j = [load, key, hand, finger, steps]
        v_ref = [0.0341, 1.0, 0.4980, 0.1401, 1.4516, 0.1632, 4.05]
        weights = [0.45, 0.5, 1, 0.8, 0.7]
        return sum([weights[i] * v_j[i] / v_ref[i] for i in range(5)])

    def recombine(self, other):
        new_dict, new_design = {}, self.__empty_design__()
        p = 0.5
        k = int(len(self.alphabet) * p)
        keys = self.__select_k_keys__(k)
        for (k, [h,x,y]) in keys:
            new_dict.update({k : [h,x,y]})
            new_design[x][y] = k
        keys_left = other.__keys_complement__(new_dict)
        self.__complete_keyboard__(new_dict, new_design, keys_left)
        return Layout(coordinates=new_dict,
                      design=new_design)

    def mutate(self, letter1, letter2):
        [h1,x1,y1] = self.coordinates[letter1]
        [h2,x2,y2] = self.coordinates[letter2]

        self.coordinates[letter1] = [h2,x2,y2]
        self.coordinates[letter2] = [h1,x1,y1]
        self.design[x2][y2] = letter1
        self.design[x1][y1] = letter2

    def random_layout(self):
        pairs = []
        for row in [i for i in range(self.rows)]:
            for col in [i for i in range(self.cols)]:
                hand = 0 if col < self.cols / 2 else 1
                pairs.append([hand, row, col])
        positions = {}
        for c in self.alphabet:
            i = rnd.randint(0, len(pairs) - 1)
            positions.update({c : pairs[i]})
            del pairs[i]
        return positions

    def copy(self):
        coordinates = self.coordinates
        design = self.design
        alphabet = self.alphabet
        return Layout(self.coordinates.copy(),
                      self.design[:],
                      self.alphabet[:])

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __no_big_steps__(self):
        steps_sum = 0
        for bigram in self.bigrams:
            mngr1 = utils_no_accent(bigram[0])
            mngr2 = utils_no_accent(bigram[1])
            [h1,x1,y1] = self.coordinates[mngr1]
            [h2,x2,y2] = self.coordinates[mngr2]
            f1 = utils_finger_by_column(y1)
            f2 = utils_finger_by_column(y2)
            if h1 == h2 and f1 != f2:
                if utils_vertical_distance((x1,y1), (x2,y2)) >= 1:
                    coeff_weight = self.coefficients[f1][f2]
                    (frq, prc) = self.bigrams[bigram]
                    steps_sum += coeff_weight * prc
        return steps_sum

    def __same_finger_and_hand__(self):
        same_usage = 0
        for bigram in self.bigrams:
            mngr1 = utils_no_accent(bigram[0])
            mngr2 = utils_no_accent(bigram[1])
            [h1,x1,y1] = self.coordinates[mngr1]
            [h2,x2,y2] = self.coordinates[mngr2]
            f1 = utils_finger_by_column(y1)
            f2 = utils_finger_by_column(y2)
            if h1 == h2 and f1 == f2:
                (freq, perc) = self.bigrams[bigram]
                dist = utils_manhattan_distance((x1,y1), (x2,y2))
                same_usage += perc * dist
        return same_usage

    def __hand_alternation__(self):
        hand_sum = 0
        for bigram in self.bigrams:
            mngr1 = utils_no_accent(bigram[0])
            mngr2 = utils_no_accent(bigram[1])
            [h1,x1,y1] = self.coordinates[mngr1]
            [h2,x2,y2] = self.coordinates[mngr2]
            if h1 == h2:
                (frq, perc) = self.bigrams[bigram]
                hand_sum += perc
        return hand_sum

    def __load_distribution__(self):
        load_sum = 0
        for monogram in self.monograms:
            opt = self.__ideal_load_distribution__(monogram)
            (frq, perc) = self.monograms[monogram]
            load_sum += (opt - perc) ** 2
        return load_sum

    def __ideal_load_distribution__(self, monogram):
        hand_weight = 0.5
        col_map = lambda x : [5,4,3,2,1,1,2,3,4,5][x]
        row_map = lambda x : x + 2
        monogram = utils_no_accent(monogram)
        [h,x,y] = self.coordinates[monogram]
        row_load = self.load_distribution[row_map(x)][0]/100.0
        col_load = self.load_distribution[col_map(y)][1]/100.0
        return  hand_weight * row_load * col_load

    def __add_keys__(self, keys):
        '''  '''
        for (k, pos) in keys:
            self.coordinates[k] = pos

    def __complete_keyboard__(self, new_dict, new_design, keys_left):
        ''' Rellena el layout con las letras faltantes keys_left '''
        for row in range(self.rows):
            for col in range(self.cols):
                if not keys_left: break
                if new_design[row][col] == ' ':
                    (k, [h,x,y]) = keys_left.pop(0)
                    new_design[row][col] = k
                    h = 0 if col < self.cols / 2 else 1
                    new_dict.update({k:[h,row,col]})

    def __keys_complement__(self, keys):
        '''
            Obtiene las llaves self.alfabeto - keys en orden
            del teclado self.
        '''
        complement = []
        for row in range(self.rows):
            for col in range(self.cols):
                k = self.design[row][col]
                if k != ' ':
                    if k not in keys:
                        complement.append(k)
                else:
                    h = 0 if col < self.cols / 2 else 1
                    complement.append((k,[h,row,col]))
        return [(k,self.coordinates[k]) if isinstance(k,str) else k
                                        for k in complement]
    def __select_k_keys__(self, k):
        '''
            Selecciona k letras aleatorias del alfabeto.
            Regresa una lista [(letra, [h,x,y])] donde
            [h,x,y] es self.coordinates[letra]
        '''
        seen = set([])
        bound = len(self.alphabet) - 1
        while len(seen) < k:
            i = rnd.randint(0, bound)
            seen.add(self.alphabet[i])
        return [(k, self.coordinates[k]) for k in list(seen)]

    def __empty_design__(self):
        '''
            Obtiene un layout vacío.
            Cada entrada del arreglo contiene " "
        '''
        design = [[" " for i in range(self.cols)]
                       for j in range(self.rows)]
        return design

    def __to_array__(self):
        arrangement = self.__empty_design__()
        for key in self.coordinates:
            [h,r,c] = self.coordinates[key]
            arrangement[r][c] = key
        return arrangement

    def __eq__(self, other):
        if not isinstance(other, Layout):
            raise TypeError
        return self.fitness == other.fitness

    def __lt__(self, other):
        if not isinstance(other, Layout):
            raise TypeError
        return self.fitness < other.fitness

    def __gt__(self, other):
        if not isinstance(other, Layout):
            raise TypeError
        return self.fitness > other.fitness

    def __str__(self):
        arrangement = self.__to_array__()
        string = "Fitness: %f\n" % self.fitness
        space = 1
        for row in range(self.rows):
            for col in range(self.cols):
                string += "%s " % (arrangement[row][col])
            string += "\n" + " "*space
            space += 1
        return string

if __name__ == '__main__':
    layout = Layout()
    r = Layout()
    print(r)
    print(layout)
    print(r.__load_distribution__())
