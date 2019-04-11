def solution1(arg):
    return [i * 4 for i in arg]

def solution2(arg):
    return [(i+1) * char for i, char in enumerate(arg)]

def solution3(arg):
    return [i for i in arg if i % 5 == 0 or i % 3 == 0]

def solution4(arg):
    return [i for subarg in arg for i in subarg]

def solution5(arg):
    n = range(1, arg + 1 )
    return [
        (i, j, k) 
        for i in n 
            for j in n 
                for k in n 
                    if i * i + j * j == k * k and i <= j and j <= k
    ]

def solution6(arg):
    return [[i + j  for j in arg[1]] for i in arg[0]]

def solution7(arg):
    return [[arg[j][i] for j in range(len(arg))] for i in range(len(arg[0]))]

def solution8(arg):
    return [list(map(int, str.split())) for str in arg]

def solution9(arg):
    return {chr(ord('a') + i): i * i for i in arg}

def solution10(arg):
    return set(name.lower().capitalize() for name in arg if len(name) > 3) 

solutions = {
    'solution1': solution1,
    'solution2': solution2,
    'solution3': solution3,
    'solution4': solution4,
    'solution5': solution5,
    'solution6': solution6,
    'solution7': solution7,
    'solution8': solution8,
    'solution9': solution9,
    'solution10': solution10,
}

if __name__ == '__main__':
    args = [
        'python',
        'python',
        range(16),
        [[1, 2, 3], [4, 5, 6, 7], [8, 9], [0]],
        15,
        ([0, 1, 2], [0, 1, 2, 3, 4]),
        [[1, 3, 5], [2, 4, 6]],
        ["0", "1 2 3", "4 5 6 7", "8 9"],
        range(0, 7),
        ['Alice', 'vova', 'ANTON', 'Bob', 'kAMILA', 'CJ', 'ALICE', 'Nastya']
    ]
