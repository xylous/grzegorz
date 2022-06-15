from .word import Word, readfile, writefile

import json

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

def differences(word1, word2):
    ipa1 = word1.ipa
    ipa2 = word2.ipa
    count = sum(1 for a, b in zip(ipa1, ipa2) if a != b)
    return count

def format_tuple(tuple):
    return '{} - {}'.format(tuple[0].text, tuple[1].text)
