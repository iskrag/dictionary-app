import functions as func

file = 'Svenska_ordbok.txt'
# file = 'test.txt'

words_dict = func.process_dict(file)
while True:
    random_word = func.generate_swe_word(words_dict)
    print('Swedish word: ' + random_word.upper())
    eng_guess = input('English translation: ')
    count = func.check_guess(eng_guess, words_dict, random_word)
    if count > 0 and len(words_dict[random_word]) > 1:
        synonym = input('Enter synonym: ')
        func.check_guess(synonym, words_dict, random_word, syn=1)
