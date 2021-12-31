import re
import pickle
import itertools
from collections import Counter
import json


with open('src/pickle/models.pkl', 'rb') as file:
    vocab = pickle.load(file)
    
words = list(vocab)
    
w_rank = {}
for iter,word in enumerate(words):
    w_rank[word] = iter
        
WORDS = w_rank

dict(itertools.islice(WORDS.items(), 10))


def words(text): return re.findall(r'\w+', text.lower())


def P(word): 
    "Probability of `word`."
    # use inverse of rank as proxy
    # returns 0 if the word isn't in the dictionary
    return - WORDS.get(word, 0)

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

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


with open("src/source/slang_corpus.txt") as f:
    slangS = json.loads(f.read())
    
with open("src/source/formal.txt") as f:
    formalS = json.loads(f.read())
    
    
def typechecker(T):
    Texts = re.findall(r"[\w']+|[.,!?;]",T)
    
    _spelling = []
    for text in Texts:
        _spelling.append(correction(text))
    
    for index,text in enumerate(_spelling):
        if text in slangS.keys():
            _spelling[index] = slangS[text]

    for index,text in enumerate(_spelling):
        if text in formalS.keys():
            _spelling[index] = formalS[text]
              
    _text = ' '.join(_spelling)
    _text = re.sub(r' ([^A-Za-z0-9])', r'\1', _text)
    
    return _text
