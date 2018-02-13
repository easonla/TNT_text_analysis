## spelling correction
import re
import enchant
from collections import Counter
chkr = enchant.Dict('en_US')

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('data/BigUNcorpora.txt').read()))
#WORDS = Counter(words(open('data/big.txt.txt').read()))


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    try:
        return WORDS[word] / N
    except:
        return 0

def correction(word): 
    "Most probable spelling correction for word."
    "To reduce computational load, skip the number/known word/one character"
    if re.search(r'\d+',word): 
        return word
#     elif len(word) == 1:
#         return word
#     elif len(known([word])) == 0 : 
#         return word
    else:
        return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word] or chkr.suggest(word))

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))