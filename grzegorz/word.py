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

class Sound:
    """ Aside from a mere noise, a sound can also be long or short """
    def __init__(self, sound: str, long: bool):
        self.sound = sound
        self.long = long

    def __eq__(self, other) -> bool:
        return self.sound == other.sound and \
                self.long == other.long

    def __str__(self) -> str:
        long = ""
        if self.long:
            long = ":"
        return '"' + self.sound + long + '"'

class Syllable:
    """
    A syllable is composed of one or several sounds and can have various types
    of stress
    """
    def __init__(self, stress: str, sounds: list[Sound]):
        self.stress = stress
        self.contents = sounds

    def __eq__(self, other) -> bool:
        return self.stress == other.stress and \
                self.contents == other.contents

    def __str__(self) -> str:
        return "(" + repr(self.contents) + "; " + self.stress + ")"

class Word:
    """
    All we care about is the word's text and its IPA
    """
    def __init__(self, text: str, ipa: str) -> None:
        self.text = text
        self.ipa = ipa
        self.phonology = []

    def get_ipa(self, language: str):
        """
        Look on the English Wiktionary for the IPA of the current word; if it
        has one, then fill its `ipa` property, otherwise don't
        """
        parser = WiktionaryParser()
        parser.set_default_language(language)
        # If we get no result, skip.
        try:
            ipa = first_ipa_pronunciation(parser.fetch(self.text)[0]['pronunciations']['text'][0])
            # Remove leading and trailing `/`, `[` and `]`
            ipa = re.sub(r"[/\[\]]", "", ipa)
            # Not all words have their IPAs on wiktionary, but they might have a
            # "Rhymes" section (try German wordlists). If we did fetch a rhyme,
            # don't add it as a valid IPA
            if ipa[0] != '-':
                self.ipa = ipa
        except (IndexError, AttributeError) as _:
            pass
        return self

    @staticmethod
    def obj_dict(word):
        """Return this class as a dictionary"""
        dict = word.__dict__
        # this might fail since the dictionary is mutated, and the same Word
        # might be converted more than one time
        try:
            # We don't need to know about the sounds of the word; those can be
            # computed
            dict.pop('phonology')
        except KeyError:
            pass
        return dict

    @staticmethod
    def from_dict(dict) -> 'Word':
        """Deserialise this class from JSON"""
        return Word(dict['text'], '/' + dict['ipa'] + '/')

class MinPair:
    """Two words in a pair. Voilà c'est tout."""
    def __init__(self, first: Word, last: Word) -> None:
        self.first = first;
        self.last = last;

    @staticmethod
    def obj_dict(obj: 'MinPair'):
        """Return this class as a dictionary"""
        dict = obj.__dict__;
        dict['first'] = Word.obj_dict(dict['first']);
        dict['last'] = Word.obj_dict(dict['last']);
        return dict

    @staticmethod
    def from_dict(dict) -> 'MinPair':
        """Construct this class from a dictionary"""
        word1 = Word.from_dict(dict['first'])
        word2 = Word.from_dict(dict['last'])
        return MinPair(word1, word2)

### Helper functions ###

def first_ipa_pronunciation(ipa_str: str) -> str:
    """Find the first IPA spelling in the given string"""
    return re.findall(r"[/\[].*?[/\]]", ipa_str)[0]

def readfile(path: str) -> str:
    """Return the contents of a file"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def writefile(path: str, text: str) -> None:
    """Write `text` to the given path"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
