from list_of_words import words
from display_game import man_hanging
import random
import string

def get_right_word(word):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = get_right_word(words)
    word_letters = set(word)  # Letters in the word
    alpha = set(string.ascii_uppercase)
    used_alphas = set()  # Letters user has guessed
    chances = 7
    # getting user input
    while len(word_letters) > 0 and chances > 0:
        # Letters Used
        print('YOU HAVE', chances, 'CHANCES LEFT TO GUESS AND YOU HAVE USED THESE LETTERS: ', ' '.join(used_alphas))

        # Hangman word
        word_list = [letter if letter in used_alphas else '_' for letter in word]
        print(man_hanging[chances])
        print('HANGMAN WORD: ', ' '.join(word_list))

        user_alpha = input('Guess a Letter: ').upper()
        if user_alpha in alpha - used_alphas:
            used_alphas.add(user_alpha)
            if user_alpha in word_letters:
                word_letters.remove(user_alpha)
            else:
                chances = chances - 1
                print("LETTER NOT IN THE WORD!!")

        elif user_alpha in used_alphas:
            print("YOU HAVE ALREADY GUESSED THIS LETTER, PLEASE TRY AGAIN")

        else:
            print("INVALID ALPHABET!!, TRY AGAIN")
    #
    if chances == 0:
        print(man_hanging[chances])
        print("MAN WAS HANGED !!, YOU FAILED!!", word)
    else:
        print('YOU ARE RIGHT!!', word, ':) :)')


if __name__ == '__main__':
    hangman()
