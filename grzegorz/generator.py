from .word import Word, readfile, writefile
import json

# Given the path to a file containing JSON data about serialised `Word`s, create
# a file `outfile` with all the minimal pairs found
def createpairs(infile, outfile):
    jsonstr = readfile(infile)
    words = json.loads(jsonstr, object_hook=Word.fromJSON)
    minpairs = []
    for i in range(0,len(words)):
        w1 = words[i]
        for j in range(i+1,len(words)):
            w2 = words[j]
            if w1.ipa == w2.ipa or len(w1.ipa) != len(w2.ipa):
                continue
            diffs = differences(w1, w2)
            if diffs == 1:
                minpairs.append((w1, w2))
    formatted = list(map(format_tuple, minpairs))
    writefile(outfile, '\n'.join(str(x) for x in formatted))
    print('Done! Generated', len(minpairs), 'minimal pairs')

### Helper functions ###

# Return the number of differences between words
def differences(word1, word2):
    ipa1 = word1.ipa
    ipa2 = word2.ipa
    count = sum(1 for a, b in zip(ipa1, ipa2) if a != b)
    return count

# Format a tuple containing two words so that it's human-readable
def format_tuple(tuple):
    return '{} - {}'.format(tuple[0].text, tuple[1].text)
