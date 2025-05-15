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
    """Check if the guess matches any translation or synonym (case-insensitive)."""
    # Split answers and normalize to lowercase for comparison
    answers = [meaning.strip() for meaning in
               re.split(r',\s*|/', d[key][syn].strip())]
    normalized_answers = [ans.casefold() for ans in answers]
    normalized_guess = word.strip().casefold()

    result = {}
    if normalized_guess in normalized_answers:
        result['status'] = 'correct'
        counter += 1
        # Preserve original casing for display
        if '/' in d[key][syn]:
            result['full_answer'] = [m.strip().upper() for m in
                                     d[key][syn].split('/')]
        elif ',' in d[key][syn]:
            result['full_answer'] = [d[key][syn].upper()]
        else:
            result['full_answer'] = [d[key][syn].upper()]
    else:
        result['status'] = 'incorrect'
        if '/' in d[key][syn]:
            result['full_answer'] = [m.strip().upper() for m in
                                     d[key][syn].split('/')]
        else:
            result['full_answer'] = [d[key][syn].upper()]

    result['counter'] = counter
    return result


def check_guess(guess, d, key, syn=0):
    """Check if a guess is correct for translation or synonym."""
    guesses = split_guess(guess)
    if not guesses:
        return {
            'status': 'invalid',
            'message': 'No valid answer given.',
            'full_answer': [d[key][syn].upper()],
            'counter': 0
        }
    counter = 0
    for word in guesses:
        result = check_translation_or_synonym(d, key, word, syn, counter)
        if result['status'] == 'correct':
            return result
    # If none correct, return last result (which will be incorrect)
    return result


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
