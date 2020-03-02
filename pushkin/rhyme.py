import operator
import re
from functools import lru_cache

from collections import defaultdict
from tqdm import tqdm_notebook, tqdm

from pymorphy2 import MorphAnalyzer
import pickle

import random
import numpy as np


VOWELS_LOWER = 'аоуыэяёюие'
VOWELS_UPPER = VOWELS_LOWER.upper()
MA = MorphAnalyzer()
KS = [4, 3, 2]


def strip_all(line):
    return re.sub('[^a-zA-Zа-яА-ЯёЁ ]+', '', line).lower()


def get_last_word(line):
    return strip_all(line).split()[-1]


def apostrophe2capital(word):
    """ Transform 'п`ушка' to 'пУшка' """
    result = ''
    next_big = False
    for letter in word: 
        if letter == '`':
            next_big = True
        else:
            if next_big:
                letter = letter.upper()
                next_big = False
            result = result + letter
    return result

def where_accent_first(word):
    vowels_before = 0
    for letter in word:
        if letter in VOWELS_LOWER:
            vowels_before += 1
        if letter in VOWELS_UPPER:
            return vowels_before
    # by default, it is last
    return max(0, vowels_before-1)
    

def accent_last(word, k=0):
    result = ''
    vowels_before = 0
    for letter in word[::-1]:
        if letter in VOWELS_LOWER:
            if vowels_before == k:
                letter = letter.upper()
            vowels_before += 1
        result = letter + result
    if vowels_before > 0 and vowels_before < k:
        return accent_first(word)
    return result


def accent_first(word, k=0):
    result = ''
    vowels_before = 0
    for letter in word:
        if letter in VOWELS_LOWER:
            if vowels_before == k:
                letter = letter.upper()
            vowels_before += 1
        result = result + letter
    if vowels_before > 0 and vowels_before < k:
        return accent_last(word)
    return result


def get_rythm(sentence):
    ans = []
    for letter in sentence:
        if letter in VOWELS_LOWER:
            ans.append(0)
        elif letter in VOWELS_UPPER:
            ans.append(1)
    return ans


def find_rhyme(line, dicts, accentor, suffix_lenghts=KS, accented=False):
    words = strip_all(line).split()
    if accented:
        words = [accentor.add_accent(word) for word in words]
    stripped = ''.join(words)
    if accented:
        rythm = get_rythm(stripped)
    last_word = words[-1]
    
    for k in suffix_lenghts:
        last = stripped[-k:]
        ans = dicts[k][last]
        # нельзя рифмовать тем же самым словом
        if not accented:
            ans = [a for a in ans if get_last_word(a) != last_word]
            if ans:
                return ans
        else:
            ans = [(a[0], a[1], backward_match(rythm, get_rythm(a[1]))) 
               for a in ans if get_last_word(a[0]).lower() != last_word.lower()]
            if ans:
                return sorted(ans, key=operator.itemgetter(2), reverse=True)
    return []


def backward_match(pat1, pat2):
    ans = 0
    for el1, el2 in zip(pat1[::-1], pat2[::-1]):
        if el1 == el2:
            ans += 1
    return ans


class Accentor:
    def __init__(self, dictionary):
         self.dictionary=dictionary
    
    @lru_cache(maxsize=10000)
    def add_accent(self, word, default='capital'):
        num_letters = len(word)
        num_vowels = len(re.sub('[^аоуыэяёюие]+', '', word))
        if num_letters <= 2:
            # small words are not accented
            return word
        if num_vowels <= 1:
            return accent_first(word)
        if word in self.dictionary:
            return self.dictionary[word][0]
        nf = MA.parse(word)[0].normal_form
        if nf in self.dictionary:
            nf_accent, other_forms, right = self.dictionary[nf]
            if word in other_forms:
                return other_forms[word]
            where = where_accent_first(nf_accent)
            return accent_first(word, where)
        # если ничего не нашли, просто возвращаем ударение на последний слог
        if default == 'capital':
            return word.upper()
        elif default == 'last':
            return accent_last(word)
        if default == 'first':
            return accent_first(word)
        else: # default = 'none
            return word


class Rhymer:
    def __init__(self, simple_dicts, accented_dicts, dictionary, decay=0.3):
        self.decay = decay
        self.simple_dicts = simple_dicts
        self.accented_dicts = accented_dicts
        self.accentor = Accentor(dictionary)

    def random_rhyme(self, phrase):
        results = find_rhyme(phrase, dicts=self.accented_dicts, accented=True, accentor=self.accentor)
        if not results:
            results = find_rhyme(phrase, dicts=self.simple_dicts, accented=False, accentor=self.accentor)
            if results:
                return results[0]
            return 'увы, не получилось'
        best = results[0][2]
        if self.decay == 0:
            best_results = [r[0] for r in results if r[2]==best]
            return best_results[random.randint(0, len(best_results)-1)]
        else: # 0 < decay <= 1
            probas = [self.decay**(r[2]-best) for r in results]
            probas = np.array(probas) / sum(probas)
            return np.random.choice([r[0] for r in results], p=probas)


if __name__ == '__main__':
    lop1 = dict()
    with open('lop1v2.txt', 'r', encoding='cp1251') as f:
        for l in f.readlines():
            left, midright = l.strip().split('#')
            mid, right = midright.split('%')
            other_forms = {}
            for r in right.split(','):
                stripped = apostrophe2capital(r.strip())
                other_forms[stripped.lower()] = stripped
            for k, v in other_forms.items():
                lop1[k] = v, {}, ''
            lop1[left] = apostrophe2capital(mid), other_forms, right

    accentor = Accentor(lop1)
    pu_fn = 'pushkins.txt'

    with open(pu_fn, 'r', encoding='cp1251') as f:
        lines = [l.strip() for l in f.readlines() if len(l.strip()) >= 4]

    reverse_dicts = {k: defaultdict(list) for k in KS}
    accented_dicts = {k: defaultdict(list) for k in KS}

    for l in tqdm(lines):
        words = strip_all(l).split()
        accented_words = [accentor.add_accent(word) for word in words]
        stripped = ''.join(words)
        stripped_accented = ''.join(accented_words)
        for k in KS:
            last = stripped[-k:]
            reverse_dicts[k][last].append(l)
            last = stripped_accented[-k:]
            accented_dicts[k][last].append([l, stripped_accented])
    with open('pushkin.pkl', 'wb') as f:
        pickle.dump([reverse_dicts, accented_dicts, lop1], f)
    print('Success!')

