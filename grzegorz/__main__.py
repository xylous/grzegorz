from wiktionaryparser import WiktionaryParser
from multiprocessing import Pool
from os.path import exists

import json

class Word:
    def __init__(self, text, ipa):
        self.text = text
        self.ipa = ipa

    def get_ipa(self):
        print("Processing '", self.text, "'", sep="")
        parser = WiktionaryParser()
        word = parser.fetch(self.text, 'polish')
        # If we get no result, skip.
        try:
            pron = word[0]['pronunciations']
            self.ipa = lastword(pron['text'][0])
        except:
            self.ipa = ''
        return self

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    @staticmethod
    def fromJSON(json_dct):
        return Word(json_dct['text'], json_dct['ipa'])

    def __repr__(self):
        return "<Word text:%s ipa%s>" % (self.text, self.ipa)

    def __str__(self):
        return "(%s %s)" % (self.text, self.ipa)

def dict_has_key(dict, key):
    return key in dict.keys()

def lastword(str):
    words = str.split()
    return words[-1]

def readfile(path):
    f = open(path, 'r')
    return f.read()

def writefile(path, txt):
    f = open(path, 'w')
    f.write(txt)
    f.close()
    return

def list_to_words(str):
    # Remove empty lines
    words = [Word(x, '') for x in str.splitlines() if x]
    return words

def differences(word1, word2):
    ipa1 = word1.ipa
    ipa2 = word2.ipa
    count = sum(1 for a, b in zip(ipa1, ipa2) if a != b)
    return count

def format_tuple(tuple):
    return '{} - {}'.format(tuple[0].text, tuple[1].text)

def proc_files():
    jsonstr = readfile("list.json")
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
    writefile("out.txt", '\n'.join(str(x) for x in formatted))
    print('Done. Check out.txt')

def main():
    if exists("list.json"):
        proc_files()
        return

    numproc = 20

    contents = readfile("list.txt")
    words = list_to_words(contents)

    with Pool(numproc) as p:
        wds = p.map(Word.get_ipa, words)

    jsonlog = json.dumps([word.__dict__ for word in wds])
    writefile("list.json", jsonlog)

    print('Done!!!')

main()
