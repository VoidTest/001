import random

def making_a_guess():
    global update_display
    correct_guess = False
    for i, letter in enumerate(chosen_word):
        if guess.lower() == letter:
            blank_list[i] = guess.lower()
            correct_guess = True
    if not correct_guess:
        print(f"There is no {guess}, sorry.")
        update_display += 1

HANGMANPICS = ['''  +---+  |   |      |      |      |      |=========''', '''  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

word_list = ["aardvark", "baboon", "camel", "jazz", "grass", "follow", "castle", "cloud"]
chosen_word = list(random.choice(word_list))
blank_list = ["_" for _ in chosen_word]

update_display = 0

print(HANGMANPICS[update_display])
print("Welcome to hangman.")
print("".join(blank_list))

while update_display < 6:
    guess = input("Make a guess? ")
    making_a_guess()
    print(HANGMANPICS[update_display])
    print("".join(blank_list))
    if blank_list == chosen_word:
        print("YOU WIN!")
        break

if update_display == 6:
    print("GAME OVER.")
