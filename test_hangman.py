import random
from hangman_art import logo, stages
from hangman_words import word_list

target_word = random.choice(word_list)

print(target_word)
guess_list = list("-" * len(target_word))

print(guess_list)

count = 0

while count < len(stages):
    for char in target_word:
        guess_char = input("Please input your guess: ")
        if char == guess_char:
            guess_list[target_word.index(char)] = guess_char
            count += 1
            print(guess_list)
        else:        
            print(stages[count])



