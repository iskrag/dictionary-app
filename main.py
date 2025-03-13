import re
import unicodedata
import random

"""A little dictionary to help improve my Swedish vocabulary."""


def clean_word(word):
    """Normalize and remove soft/non-breaking hyphens from words."""
    word = unicodedata.normalize("NFKC", word)
    return word.replace("\u00AD", "").replace("\u2011",
                                              "-")  # Soft & non-breaking hyphens


def split_meanings(word):
    """Split the different meanings of a word."""
    meanings = word.split('/')
    for ind, meaning in enumerate(meanings):
        print(f"{ind+1}. " + meaning)


def generate_swe_word(d):
    """Generate a random word from the """
    word = random.choice(list(d))
    return word


def check_guess(guess, d, key, syn=0):
    """Check if a guess is correct."""
    counter = 0
    split_guess = [word for word in re.split(r', |; ', guess.strip()) if word]

    if not split_guess:  # If user input was empty or only spaces
        print("INCORRECT! No valid answer given.")
        print('The correct answer is: ' + d[key][0].upper() if syn == 0 else
              d[key][1].upper())
        return counter

    for word in split_guess:
        if syn == 0:
            if word in d[key][0]:
                print(word + ' is a correct answer!')
                counter += 1
            else:
                print(word + ' is INCORRECT!')
                print('The correct answer is: ' + d[key][0].upper())
                return counter
        elif syn == 1:
            if word in d[key][1]:
                print(len(d[key][1]))
                print(word + ' is a correct answer!')
                counter += 1
            else:
                print(word + ' is INCORRECT.')
                print('The correct answer is: ' + d[key][1].upper())
                return counter
    return counter


def process_dict(dict_file):
    words_dict = {}
    """Split each dictionary line into individual segments for further use."""
    with open(dict_file, encoding='utf-8') as f:
        for line in f:
            split_line = re.split(r': |; ', line.strip())
            if len(split_line) < 2:
                continue  # Skip malformed lines
            swe_word, eng_word = clean_word(split_line[0]), clean_word(split_line[1])
            words_dict[swe_word] = [eng_word]
            # print(swe_word, eng_word)
            # if '/' in line:
            #     split_meanings(eng_word)
            if ';' in line:
                syn = clean_word(split_line[2])
                words_dict[swe_word].append(syn)
    return words_dict


file = 'Svenska_ordbok.txt'
# file = 'test.txt'


words_dict = process_dict(file)
while True:
    random_word = generate_swe_word(words_dict)
    print('Swedish word: ' + random_word.upper())
    eng_guess = input('English translation: ')
    count = check_guess(eng_guess, words_dict, random_word)

    if count > 0 and len(words_dict[random_word]) > 1:
        synonym = input('Enter synonym: ')
        check_guess(synonym, words_dict, random_word, syn=1)
