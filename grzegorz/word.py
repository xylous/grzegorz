from wiktionaryparser import WiktionaryParser
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

### Helper functions ###

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
