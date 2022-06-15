from wiktionaryparser import WiktionaryParser
import json

# All we care about is the word's string and its IPA, its textual representation
class Word:
    def __init__(self, text, ipa):
        self.text = text
        self.ipa = ipa

    # Return a copy of the current file with foo
    def get_ipa(self):
        print("Processing '", self.text, "'", sep="")
        parser = WiktionaryParser()
        word = parser.fetch(self.text, 'polish')
        # If we get no result, skip.
        try:
            pron = word[0]['pronunciations']
            self.ipa = last_word(pron['text'][0])
        except:
            self.ipa = ''
        return self

    # Serialise this class to JSON
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    # Deserialise this class from JSON
    @staticmethod
    def fromJSON(json_dct):
        return Word(json_dct['text'], json_dct['ipa'])

    def __repr__(self):
        return "<Word text:%s ipa%s>" % (self.text, self.ipa)

    def __str__(self):
        return "(%s %s)" % (self.text, self.ipa)

### Helper functions ###

# Return the last word in a string
def last_word(str):
    words = str.split()
    return words[-1]

# Return the contents of a file
def readfile(path):
    f = open(path, 'r')
    return f.read()

# Write `txt` to the given path
def writefile(path, txt):
    f = open(path, 'w')
    f.write(txt)
    f.close()
    return
