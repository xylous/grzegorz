from .word import Word, readfile, writefile
from multiprocessing import Pool
from functools import partial
import json

# Given an input file containing a list of words separated
def fetchpron(infile, outfile, language):
    numproc = 20

    contents = readfile(infile)
    words = input_to_words(contents)

    with Pool(numproc) as p:
        wds = p.map(partial(Word.get_ipa, language=language), words)

    jsonlog = json.dumps([word.__dict__ for word in wds])
    writefile(outfile, jsonlog)

    print('Done!')

# Turn the read input into a list of `Word`s
def input_to_words(strs):
    # Remove empty lines
    words = [Word(x, '') for x in strs.splitlines() if x]
    return words
