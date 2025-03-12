import re

file = 'Svenska_ordbok.txt'

with open(file, encoding='utf-8') as f:
    for line in f:
        split_line = re.split(r': |; ', line)
        swe_word, eng_word = split_line[0], split_line[1]
        # print(swe_word, eng_word)
        if ';' in line:
            synonym = split_line[2]
            print(synonym)
