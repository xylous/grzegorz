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
import re

# All we care about is the word's string and its IPA, its textual representation
class Word:
    def __init__(self, text: str, ipa: str) -> None:
        self.text = text
        self.ipa = ipa
        self.sounds = []

    def set_sounds(self, sounds: list[str]) -> None:
        self.sounds = sounds

    # Return a copy of the current file with foo
    def get_ipa(self, language: str):
        parser = WiktionaryParser()
        parser.set_default_language(language)
        # If we get no result, skip.
        try:
            ipa = parse_ipa_pronunciation(parser.fetch(self.text)[0]['pronunciations']['text'][0])
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

    # Return this class as a dictionary
    @staticmethod
    def obj_dict(word):
        dict = word.__dict__
        # this might fail since the dictionary is mutated, and the same Word
        # might be converted more than one time
        try:
            # We don't need to know about the sounds of the word; those can be
            # computed
            dict.pop('sounds')
        except:
            pass
        return dict

    # Deserialise this class from JSON
    @staticmethod
    def from_dict(dict) -> 'Word':
        return Word(dict['text'], dict['ipa'])

    def __repr__(self) -> str:
        return "<Word text:%s ipa%s>" % (self.text, self.ipa)

    def __str__(self) -> str:
        return "(%s %s)" % (self.text, self.ipa)

# Two words in a pair. Voilà c'est tout.
class MinPair:
    def __init__(self, first, last) -> None:
        self.first = first;
        self.last = last;
        # The IPA pronunciations given to this class aren't going to be pure
        # strings, rather arrays of sounds...
        #
        # ...smells like someone's cooking spaghetti in here.
        self.first.ipa = ''.join(first.ipa)
        self.last.ipa = ''.join(last.ipa)

    # Return this class as a dictionary
    @staticmethod
    def obj_dict(obj: 'MinPair'):
        dict = obj.__dict__;
        dict['first'] = Word.obj_dict(dict['first']);
        dict['last'] = Word.obj_dict(dict['last']);
        return dict

    # Construct this class from a dictionary
    @staticmethod
    def from_dict(dict) -> 'MinPair':
        word1 = Word.from_dict(dict['first'])
        word2 = Word.from_dict(dict['last'])
        return MinPair(word1, word2)

### Helper functions ###

# Find the first IPA spelling in the given string
def parse_ipa_pronunciation(ipa_str: str) -> str:
    return re.findall(r"[/\[].*?[/\]]", ipa_str)[0]

# Return the contents of a file
def readfile(path: str) -> str:
    f = open(path, 'r')
    return f.read()

# Write `txt` to the given path
def writefile(path: str, text: str) -> None:
    f = open(path, 'w')
    f.write(text)
    f.close()
    return
