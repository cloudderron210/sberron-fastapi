import random

def generate_unique_numbers(count):
    uniqe_numbers = set()

    while len(uniqe_numbers) < count:
        number = random.randint(10**5, 10**6-1)
        uniqe_numbers.add(number)

    return list(uniqe_numbers)


print(generate_unique_numbers(10000))
