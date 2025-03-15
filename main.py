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
        pass


def generate_swe_word(d):
    """Generate a random word from the """
    word = random.choice(list(d))
    return word


def split_guess(guess):
    """Split guess if guess is more than a single word."""
    new_guess = [word for word in re.split(r', |; ', guess.strip()) if word]
    return new_guess


def check_translation_or_synonym(d, key, word, guess, syn, counter):
    if any(word == meaning for meaning in re.split(r', |/', d[key][syn].strip())):
        print(guess + ' is a correct answer!')
        counter += 1
        if len(d[key][syn]) > len(guess):
            if '/' in d[key][syn]:
                print('The full answer is: ')
                split_meanings(d[key][syn].upper())
            else:
                print('The full answer is: ', d[key][syn].upper())
    else:
        print(word + ' is INCORRECT!')
        if '/' in d[key][syn]:
            print('The correct answer is: ')
            split_meanings(d[key][syn].upper())
        else:
            print('The correct answer is: ' + d[key][syn].upper())
            # if syn == 0:
                # print('Synonyms: ' + d[key][syn].upper())
    return counter


def check_guess(guess, d, key, syn=0):
    """Check if a guess is correct."""
    new_guess = split_guess(guess)
    counter = 0
    if not new_guess:  # If user input was empty or only spaces
        print("INCORRECT! No valid answer given.")
        print('The correct answer is: ' + d[key][0].upper() if syn == 0 else
              d[key][1].upper())
        return counter

    for word in new_guess:
        if syn == 0:
            counter = check_translation_or_synonym(d, key, word, guess, syn, counter)
            return counter
        elif syn == 1:
            counter = check_translation_or_synonym(d, key, word, guess, syn, counter)
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
