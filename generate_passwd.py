import random
import string

def generate_passwd(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(chars) for _ in range(length))
    return senha

length = int(input('Digite o comprimento da senha desejada: '))
password = generate_passwd(length)
print(f'Sua senha gerada é: {password}')