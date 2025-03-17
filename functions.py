import re
import unicodedata
import random


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
        print('CORRECT!')
        counter += 1
        if len(d[key][syn]) > len(guess):
            if '/' in d[key][syn]:
                print('The full answer is: ')
                split_meanings(d[key][syn].upper())
            else:
                print('The full answer is: ', d[key][syn].upper())
    else:
        print('INCORRECT!')
        if '/' in d[key][syn]:
            print('The correct answer is: ')
            split_meanings(d[key][syn].upper())
        else:
            print('The correct answer is: ' + d[key][syn].upper())
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

    """Split each dictionary line into individual segments for further use."""

    words_dict = {}
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
