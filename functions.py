import re
import unicodedata
import random


def clean_word(word):
    """Normalize and remove soft/non-breaking hyphens from words."""
    word = unicodedata.normalize("NFKC", word)
    return word.replace("\u00AD", "").replace("\u2011", "-")


def split_meanings(word):
    """Split the different meanings of a word (on / only)."""
    meanings = word.split('/')
    if len(meanings) > 1:
        for ind, meaning in enumerate(meanings):
            print(f"{ind + 1}. {meaning.strip()}")
    else:
        print(meanings[0].strip())


def generate_swe_word(d):
    """Generate a random Swedish word from the dictionary."""
    return random.choice(list(d))


def split_guess(guess):
    """Split guess into a list of words, handling commas and semicolons."""
    return [word.strip() for word in re.split(r',|;', guess.strip()) if word.strip()]


def check_translation_or_synonym(d, key, word, syn, counter):
    """Check if the guess matches any translation or synonym."""
    answers = [meaning.strip() for meaning in
               re.split(r',\s*|/', d[key][syn].strip())]
    if word.lower() in [a.lower() for a in answers]:
        print('CORRECT!')
        counter += 1
        # Show full answer if there are multiple (comma or slash separated)
        if '/' in d[key][syn]:
            print('The full answer is:')
            split_meanings(d[key][syn].upper())
        elif ',' in d[key][syn]:
            print('The full answer is:', d[key][syn].upper())
    else:
        print('INCORRECT!')  # Removed "No valid answer given."
        if '/' in d[key][syn]:
            print('The correct answer is:')
            split_meanings(d[key][syn].upper())
        else:
            print('The correct answer is:', d[key][syn].upper())
    return counter


def check_guess(guess, d, key, syn=0):
    """Check if a guess is correct for translation or synonym."""
    guesses = split_guess(guess)
    if not guesses:
        print('INCORRECT! No valid answer given.')
        print('The correct answer is:', d[key][syn].upper())
        return 0
    counter = 0
    for word in guesses:
        counter = check_translation_or_synonym(d, key, word, syn, counter)
        if counter > 0:
            break  # Stop after first correct guess
    return counter


def process_dict(dict_file):
    """Process the dictionary file into a usable dictionary object."""
    words_dict = {}
    with open(dict_file, encoding='utf-8') as f:
        for line in f:
            split_line = re.split(r': |; ', line.strip())
            if len(split_line) < 2:
                continue  # Skip malformed lines
            swe_word = clean_word(split_line[0])
            eng_word = clean_word(split_line[1])
            words_dict[swe_word] = [eng_word]
            if len(split_line) > 2:
                # Handle multiple synonyms separated by ';'
                synonyms = [clean_word(s) for s in split_line[2:]]
                words_dict[swe_word].extend(synonyms)
    return words_dict
