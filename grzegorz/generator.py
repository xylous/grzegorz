from .word import Word, readfile, writefile
import json

# Pairs of sounds that are easy to mishear - thus, they're *interesting*
interesting_differences = [
    # Consonants
    ('d͡ʐ', 'd͡ʑ'),
    ('d͡z', 'd͡ʑ'),
    ('d͡ʐ', 'd͡z'),
    ('d͡ʐ', 'ʂ'),
    ('d͡z', 'ʂ'),
    ('ʂ', 'd͡ʑ'),
    ('ɡʲ', 'g'),
    ('ɲ', 'n'),
    ('ɲ', 'ŋ'),
    ('ŋ', 'n'),
    ('t͡ɕ', 't͡s'),
    ('t͡ɕ', 't͡ʂ'),
    ('t͡s', 't͡ʂ'),
    ('v', 'f'),
    ('u', 'w'),
    ('x', 'h'),
    ('x', 'xʲ'),
    ('z', 'ʑ'),
    ('ʐ', 'ʑ'),
    ('z', 'ʐ'),

    # Vowels
    ('ɛ̃', 'ɛ'),
    ('ɨ', 'i'),
    ('ɔ', 'o'),
    ('ɔ̃', 'ɔ'),
    ('e', 'ɛ'),
    ('ɛ̃', 'ɔ̃'),
]

# Given the path to a file containing JSON data about serialised `Word`s, create
# a file `outfile` with all the minimal pairs found
def createpairs(infile, outfile):
    jsonstr = readfile(infile)
    words = json.loads(jsonstr, object_hook=Word.fromJSON)
    minpairs = []
    # NOTE: we must first generate all possibilities and only then filter out
    # the interesting ones because the function checking for differences might
    # miss things otherwise
    print('Generating all possible minimal pairs...')
    for i in range(0,len(words)):
        w1 = words[i]
        for j in range(i+1,len(words)):
            w2 = words[j]
            if w1.ipa == w2.ipa or len(w1.ipa) != len(w2.ipa):
                continue
            diffs = differences(w1, w2)
            if diffs == 1:
                minpairs.append((w1, w2))
    print('Filtering uninteresting pairs...')
    interesting_pairs = [x for x in map(interesting_pair, minpairs) if x]
    formatted = list(map(format_tuple, interesting_pairs))
    writefile(outfile, '\n'.join(str(x) for x in formatted))
    print('Done! Generated', len(interesting_pairs), 'minimal pairs')

### Helper functions ###

# Return the number of differences between words
def differences(word1, word2):
    ipa1 = word1.ipa
    ipa2 = word2.ipa
    count = sum(1 for a, b in zip(ipa1, ipa2) if a != b)
    return count

# Format a tuple containing two words so that it's human-readable
def format_tuple(tuple):
    w1, w2 = tuple
    return '{} {} - {} {}'.format(w1.text, w1.ipa, w2.text, w2.ipa)

# Two characters are interestingly different if they're sounds that are likely
# to be confused
def are_interestingly_different(ch1, ch2):
    for diff in interesting_differences:
        if ch1 in diff and ch2 in diff and ch1 != ch2:
            return True
    return False

# If the given pair has an interesting difference, return it. Otherwise, return
# None
def interesting_pair(tuple):
    word1, word2 = tuple
    ipa1 = word1.ipa
    ipa2 = word2.ipa
    for a, b in zip(ipa1, ipa2):
        if are_interestingly_different(a, b):
            return tuple
    else:
        return None
