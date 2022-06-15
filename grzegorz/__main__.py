from wiktionaryparser import WiktionaryParser
from multiprocessing import Pool
from os.path import exists

import argparse
import json

# All we care about is the word's string and its IPA, its textual representation
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

def create_argparser():
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')
    # 'fetchpron' subcommand
    parser_fetchpron = subparsers.add_parser('fetchpron',
            help='Fetch all IPA pronunciations for the words into a JSON file')
    parser_fetchpron.add_argument('input', type=str,
            help='file containing the list of words')
    parser_fetchpron.add_argument('output', type=str,
            help='file containing the list of words')
    # 'createpairs' subcommand
    parser_createpairs = subparsers.add_parser('createpairs',
            help='Create minimal pairs, given a JSON input file')
    parser_createpairs.add_argument('input', type=str,
            help='JSON file created by fetchpron')
    parser_createpairs.add_argument('output', type=str,
            help='JSON file created by fetchpron')
    return parser

def fetchpron(infile, outfile):
    numproc = 20

    contents = readfile(infile)
    words = list_to_words(contents)

    with Pool(numproc) as p:
        wds = p.map(Word.get_ipa, words)

    jsonlog = json.dumps([word.__dict__ for word in wds])
    writefile(outfile, jsonlog)

    print('Done!!!')

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

def main():
    parser = create_argparser()
    args = parser.parse_args()

    cmd = args.subparser_name
    infile = args.input
    outfile = args.output

    match cmd:
        case 'fetchpron':
            fetchpron(infile, outfile)
        case 'createpairs':
            createpairs(infile, outfile)

main()
