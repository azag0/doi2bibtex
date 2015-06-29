#!/usr/bin/env python3
import bibtexparser as bibtex
import sys
import re
from sciabbr import abbreviate


ignored = ['of', 'the', 'and']
corrections = {
    'Nat': 'Nature',
    'Comms': 'Communications'
}


def shorten(word):
    word, suff = re.findall(r'([^:]+)(.*)', word)[0]
    return abbreviate(word) + suff


def process(title):
    words = [corrections.get(w, w) for w in title.split()
             if w.lower() not in ignored]
    if len(words) > 1:
        words = [shorten(word) if not word.endswith('.') else word
                 for word in words]
    return ' '.join(words)


bib = bibtex.load(sys.stdin)
for item in bib.entries:
    item['journal'] = process(item['journal'])
bibtex.dump(bib, sys.stdout)
