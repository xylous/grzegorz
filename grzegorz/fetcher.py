from .word import Word, readfile, writefile

from multiprocessing import Pool

import json

def fetchpron(infile, outfile):
    numproc = 20

    contents = readfile(infile)
    words = list_to_words(contents)

    with Pool(numproc) as p:
        wds = p.map(Word.get_ipa, words)

    jsonlog = json.dumps([word.__dict__ for word in wds])
    writefile(outfile, jsonlog)

    print('Done!')

def list_to_words(str):
    # Remove empty lines
    words = [Word(x, '') for x in str.splitlines() if x]
    return words

