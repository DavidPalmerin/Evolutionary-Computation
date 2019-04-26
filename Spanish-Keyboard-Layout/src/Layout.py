import sys
import random as rnd
from Utils import *

class Layout:

    def __init__(self,
                 coordinates={},
                 design=utils_empty_design(10,3),
                 alphabet=spanish_alphabet(),
                 random=True):
        self.rows = 3
        self.cols = 10
        self.alphabet = alphabet
        if not coordinates:
            if random:
                self.coordinates = self.random_layout()
            else: self.coordinates = {}
        else: self.coordinates = coordinates
        self.design = self.__to_array__()
        self.fitness = self.eval()

    def eval(self):
        return 1

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
                      design=new_design,
                      random=False)

    def mutate(self, letter1, letter2):
        [h1,x1,y1] = self.coordinates[letter1]
        [h2,x2,y2] = self.coordinates[letter2]

        self.coordinates[letter1] = [h2,x2,y2]
        self.coordinates[letter2] = [h1,x1,y1]
        self.design[x2][y2] = letter1
        self.design[x1][y1] = letter2


    def swap(self, A, B):
        A_value = self.coordinates[A]
        self.coordinates[A] = self.coordinates[B]
        self.coordinates[B] = A_value

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
        new_layout = Layout()
        new_layout.coordinates = self.coordinates
        new_layout.design = self.design
        new_layout.fitness = self.fitness
        new_layout.alphabet = self.alphabet
        return new_layout

    def set_fitness(self, fitness):
        self.fitness = fitness

    def __add_keys__(self, key):
        for (k, pos) in keys:
            self.coordinates[k] = pos

    def __complete_keyboard__(self, new_dict, new_design, keys_left):
        for row in range(self.rows):
            for col in range(self.cols):
                if not keys_left: break
                if new_design[row][col] == ' ':
                    (k, [h,x,y]) = keys_left.pop(0)
                    new_design[row][col] = k
                    new_dict.update({k:[h,row,col]})

    def __keys_complement__(self, keys):
        complement = []
        for row in range(self.rows):
            for col in range(self.cols):
                k = self.design[row][col]
                if k != ' ' and  k not in keys:
                    complement.append(k)
        return [(k,self.coordinates[k]) for k in complement]

    def __select_k_keys__(self, k):
        seen = set([])
        bound = len(self.alphabet) - 1
        while len(seen) < k:
            i = rnd.randint(0, bound)
            seen.add(self.alphabet[i])
        return [(k, self.coordinates[k]) for k in list(seen)]

    def __empty_design__(self):
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
        string = ""
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
    new = r.recombine(layout)
    print(new)
    new.mutate('A', 'Z')
    print(new)
