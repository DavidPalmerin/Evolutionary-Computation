def spanish_alphabet():
    alphabet = [chr(i + 65) for i in range(26)]
    alphabet.append('Ñ')
    return alphabet


def utils_empty_design(rows, cols):
    design = [[" " for i in range(cols)]
                   for j in range(rows)]
    return design
