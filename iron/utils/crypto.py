import random
import string

ID_LENGTH = 32

def generate_random_item(items):
    rand = random.SystemRandom()
    return rand.choice(items)

def generate_random_id():
    alphabet = string.ascii_letters + string.digits

    attempts = [None] * 100
    for index, _ in enumerate(attempts):
        attempts[index] = ''.join([generate_random_item(alphabet) for _ in range(ID_LENGTH)])

    return generate_random_item(attempts)

