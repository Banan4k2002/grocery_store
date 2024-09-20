def first_elements(n):
    result = []
    element = 1
    while len(result) < n:
        result.extend([str(element)] * element)
        element += 1
    return ''.join(result[:n])


if __name__ == '__main__':
    n = int(input('Введите число элементов последовательности: '))
    print('Последовательность: ', first_elements(n))
