import random


def generate(wieght, hight):
    chance = []
    chance += (wieght * hight - (wieght * hight) // 50) * ['_'] + (hight * wieght) // 50 * [1]
    for i in enumerate(chance):
        if i[1] == 1:
            chance[i[0]] = f'unit-{i[0]}|'
    random.shuffle(chance)
    map_generate = [[chance[(i * wieght) + j] for j in range(wieght)] for i in range(hight)]
    return map_generate


def matrix_doc(matrix):  # matrix_determination_of_coordinates/определение координат
    coordinate_list = []
    for i in enumerate(matrix):
        for j in enumerate(i[1]):
            if j[1] != '_':
                coordinate = [j[1], f'{j[1]}_number', j[0], i[0]]
                coordinate_list.append(coordinate)
    return coordinate_list


def matrix_dtd(coordinate_list):  # matrix_determining_the_distance/определение расстояния
    distance_list = []
    exception_list = []
    for i in coordinate_list:
        temporary_list = []
        lair_list = coordinate_list[:]
        lair_list.remove(i)
        exception_list.append(i)
        for i in exception_list:
            if i in lair_list:
                lair_list.remove(i)
        for j in lair_list:
            if i[2] == j[2]:
                temporary_list.append((i[2] - j[2]) // 2) if i > j else (j[2] - i[2]) // 2
            elif i[3] == j[3]:
                temporary_list.append((i[3] - j[3]) // 2) if i > j else (j[3] - i[3]) // 2
            elif i[2] != j[2] and i[3] != j[3]:
                if i[2] > j[2] and i[3] > j[3]:
                    temporary_list.append((int(((i[2] - j[2]) ** 2 + (i[3] - j[3]) ** 2) ** 0.5)) // 2)
                elif i[2] < j[2] and i[3] > j[3]:
                    temporary_list.append((int(((j[2] - i[2]) ** 2 + (i[3] - j[3]) ** 2) ** 0.5)) // 2)
                elif i[2] > j[2] and i[3] < j[3]:
                    temporary_list.append((int(((i[2] - j[2]) ** 2 + (j[3] - i[3]) ** 2) ** 0.5)) // 2)
                elif i[2] < j[2] and i[3] < j[3]:
                    temporary_list.append((int(((j[2] - i[2]) ** 2 + (j[3] - i[3]) ** 2) ** 0.5)) // 2)
        new_distance = (min(temporary_list) if temporary_list else (max(distance_list, key=lambda x: x[3]))[
            3]) + 1 if distance_list else 1
        distance = [i[0], f'{i[1].rstrip("number")}{new_distance}', i[2], i[3], new_distance]
        distance_list.append(distance)
    return distance_list


def matrix_completion(name_2, x_position, y_position, scale, any_matrix, counter=1):  # наполнение
    while scale != 0:
        for r in range(len(any_matrix)):
            if r in range(y_position - counter, sum([y_position, counter, 1])):
                for c in range(len(any_matrix[0])):
                    if c in range(x_position - counter, sum([x_position, counter, 1])):
                        if any_matrix[r][c] == '_':
                            any_matrix[r][c] = f'{name_2.rstrip("123456780")}{scale - 1}'
        scale -= 1
        counter += 1
    return any_matrix


def connection_of_all(wieght, hight):
    matrix = generate(wieght, hight)
    matrix_new = matrix_doc(matrix)
    matrix_new = matrix_dtd(matrix_new)
    for i in enumerate(matrix_new):
        matrix = matrix_completion(i[1][1], i[1][2], i[1][3], i[1][4], matrix)
    return matrix
