# Copyright (c) 2022 xylous <xylous.e@gmail.com>
#
# This file is part of grzegorz.
# grzegorz is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# grzegorz is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# grzegorz.  If not, see <https://www.gnu.org/licenses/>.

from wiktionaryparser import WiktionaryParser
import json
import re

# All we care about is the word's string and its IPA, its textual representation
class Word:
    def __init__(self, text, ipa):
        self.text = text
        self.ipa = ipa

    # Return a copy of the current file with foo
    def get_ipa(self, language):
        parser = WiktionaryParser()
        parser.set_default_language(language)
        # If we get no result, skip.
        try:
            ipa = last_word(parser.fetch(self.text)[0]['pronunciations']['text'][0])
            # Remove leading and trailing `/`, `[` and `]`
            ipa = re.sub(r"[/\[\]]", "", ipa)
            # Not all words have their IPAs on wiktionary, but they might have a
            # "Rhymes" section (try German wordlists). If we did fetch a rhyme,
            # don't add it as a valid IPA
            if not ipa[0] == '-':
                self.ipa = ipa
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
