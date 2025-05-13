import functions as func

file = 'Svenska_ordbok.txt'
# file = 'test.txt'

words_dict = func.process_dict(file)
while True:
    random_word = func.generate_swe_word(words_dict)
    print('Swedish word: ' + random_word.upper())
    eng_guess = input('English translation: ')
    result = func.check_guess(eng_guess, words_dict, random_word)

    # Handle translation result
    if result['status'] == 'invalid':
        print('INCORRECT! No valid answer given.')
        print('The correct answer is:', result['full_answer'][0])
    elif result['status'] == 'correct':
        print('CORRECT!')
        if 'full_answer' in result and len(result['full_answer']) > 1:
            print('The full answer is:')
            for idx, ans in enumerate(result['full_answer'], 1):
                print(f"{idx}. {ans}")
        elif 'full_answer' in result:
            print('The full answer is:', result['full_answer'][0])
    else:  # incorrect
        print('INCORRECT!')
        if 'full_answer' in result and len(result['full_answer']) > 1:
            print('The correct answer is:')
            for idx, ans in enumerate(result['full_answer'], 1):
                print(f"{idx}. {ans}")
        elif 'full_answer' in result:
            print('The correct answer is:', result['full_answer'][0])

    # Ask for synonym if translation was correct and synonyms exist
    if result['status'] == 'correct' and len(words_dict[random_word]) > 1:
        synonym = input('Enter synonym: ')
        syn_result = func.check_guess(synonym, words_dict, random_word, syn=1)
        if syn_result['status'] == 'invalid':
            print('INCORRECT! No valid answer given.')
            print('The correct answer is:', syn_result['full_answer'][0])
        elif syn_result['status'] == 'correct':
            print('CORRECT!')
            if 'full_answer' in syn_result and len(
                    syn_result['full_answer']) > 1:
                print('The full answer is:')
                for idx, ans in enumerate(syn_result['full_answer'], 1):
                    print(f"{idx}. {ans}")
            elif 'full_answer' in syn_result:
                print('The full answer is:', syn_result['full_answer'][0])
        else:  # incorrect
            print('INCORRECT!')
            if 'full_answer' in syn_result and len(
                    syn_result['full_answer']) > 1:
                print('The correct answer is:')
                for idx, ans in enumerate(syn_result['full_answer'], 1):
                    print(f"{idx}. {ans}")
            elif 'full_answer' in syn_result:
                print('The correct answer is:', syn_result['full_answer'][0])
