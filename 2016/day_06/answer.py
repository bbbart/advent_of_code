from collections import defaultdict, Counter

def parse(data):
    letters_in_pos = defaultdict(list)
    for word in data:
        for pos, char in enumerate(word):
            letters_in_pos[pos].append(char)

    return letters_in_pos

def p1(data, is_sample):
    letters_in_pos = parse(data)

    word = ''
    for letters in letters_in_pos.values():
        lettercount = Counter(letters)
        letter = max(lettercount.items(), key=lambda x: x[1])[0]
        word += letter

    return word

def p2(data, is_sample):
    letters_in_pos = parse(data)

    word = ''
    for letters in letters_in_pos.values():
        lettercount = Counter(letters)
        letter = min(lettercount.items(), key=lambda x: x[1])[0]
        word += letter

    return word
