import random

words = [
    "python", 
    "programação",
    "desenvolvimento",
    "computador",
    "curso",
    "ciencia de dados",
    "inteligencia artificial"
]

choiced_word = random.choice(words)
# guessed_word = ["*"] * len(choiced_word.replace(" ", ""))
guessed_word = ["*" if x != " " else " " for x in choiced_word]
attempts = 6

print("Jogo da Forca")

while attempts > 0 and "*" in guessed_word:  # Verifica se ainda há letras para adivinhar e tentativas restantes
    print(" ".join(guessed_word))
    letter = input("Digite uma letra: ").lower()

    if letter in choiced_word:
        for i in range(len(choiced_word)):
            if choiced_word[i] == letter:
                guessed_word[i] = letter
    else:
        attempts -= 1
        print(
            f"Letra '{letter}' não encontrada. Você tem {attempts} tentativas restantes.")

if "_" not in guessed_word:
    print("Parabéns! Você venceu. A palavra era:", choiced_word)
else:
    print("Você perdeu! A palavra era:", choiced_word)