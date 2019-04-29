def spanish_alphabet():
    alphabet = [chr(i + 65) for i in range(26)]
    alphabet.append('Ñ')
    return alphabet

def utils_empty_design(rows, cols):
    design = [[" " for i in range(cols)]
                   for j in range(rows)]
    return design

def utils_load_ngrams(file_name):
    input_file = open(file_name, encoding='utf-8')
    bigrams = {}
    freqs_sum = 0
    for line in input_file.readlines():
        details = line[:-1].split(' ')
        word = details[0]
        freq = int(details[1])
        percent = float(details[2]) / 100.0
        bigrams.update({word : (freq,percent)})
        freqs_sum += freq
    return bigrams

def utils_has_accent(letter):
    return letter != utils_no_accent(letter)

def utils_no_accent(letter):
    if letter == 'Á':
        return 'A'
    if letter == 'É':
        return 'E'
    if letter == 'Í':
        return 'I'
    if letter == 'Ó':
        return 'O'
    if letter == 'Ú':
        return 'U'
    if letter == 'Ü':
        return 'U'
    return letter

def utils_manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def utils_horizontal_distance(p1, p2):
    return abs(p1[1] - p2[1])

def utils_vertical_distance(p1, p2):
    return abs(p1[0] - p2[0])

def utils_finger_by_column(col):
    new_col =  [5,4,3,2,1,1,2,3,4,5][col]
    if new_col == 1 or new_col == 2:
        return 1
    elif new_col == 3:
        return 2
    elif new_col == 4:
        return 3
    return 4

def utils_weight_coefficients():
    return [[0, 0, 0, 0, 0],
            [0, 0, 5, 8, 6],
            [0, 5, 0, 9, 7],
            [0, 8, 9, 0, 10],
            [0, 6, 7, 10, 0]]


def utils_load_distribution():
    distribution =  [ [10.87, 15.38],
                      [13.04, 10.26],
                      [15.22, 15.38],
                      [43.48, 23.08],
                      [10.87, 17.95],
                      [6.52, 6.41],
                      [1, 5.13],
                      [1, 3.85],
                      [1, 2.56]]
    return distribution

if __name__ == '__main__':
    bigrams = utils_load_ngrams('data/spanish-bigrams')
    for k in bigrams:
        print("%s %s" % (k, bigrams[k]))

    monograms = utils_load_ngrams('data/spanish-monograms')
    for k in monograms:
        print("%s %s" % (k, monograms[k]))
    print(utils_manhattan_distance((1,1), (0,0)))
