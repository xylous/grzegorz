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

import re

PHONEME_MINPAIR = 1
CHRONEME_MINPAIR = 2
STRESS_MINPAIR = 3
NOT_MINPAIR = 0

class Phone:
    """ Aside from a mere sound, a phone can also be long or short """
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
    A syllable is composed of one or several phones and can have various types
    of stress
    """
    def __init__(self, stress: str, sounds: list[Phone]):
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
        self.phonology = self.parse_phonologically()

    def print_human_readable(self) -> None:
        print(self.ipa, self.text)
        for syllable in self.phonology:
            match syllable.stress:
                case 'ˈ':
                    stress = "primary"
                case 'ˌ':
                    stress = "secondary"
                case _:
                    stress = "none"
            print("stress type:", stress)
            print("  [ ", end="")
            for sound in syllable.contents:
                print(sound, " ", sep="", end="")
            print("]")

    def parse_phonologically(self) -> list[Syllable]:
        """
        Return the phonological parse of the Word's IPA
        """
        chars = parse_ipa_characters(self.ipa)
        syllables = []
        stress = "." # assume the first syllable is unemphasised
        sounds = []

        # sometimes we need to skip characters, namely chronemes: the same sound
        # appearing consecutively is marked as one sound, but long in length
        skip = False
        for i in range(0, len(chars)):
            # don't skip if the last sound was long and we're on the last character,
            # since we need to add the sounds to a new syllable
            if skip and not (sounds[-1].long and i == len(chars) - 1):
                skip = False
                continue

            crnt = chars[i]
            next = peek(chars[i :])

            # If the current character isn't a syllable (stress) mark, then that
            # means we've encountered a sound (or a chroneme character, by accident,
            # but that's skipped). Next, figure out if the current sound is short or
            # long
            if not skip and crnt not in IPA_SYLLABLES:
                is_long_sound = False
                if next == crnt or next in IPA_CHRONEMES:
                    is_long_sound = True
                    skip = True
                # skip chroneme characters if we've accidentally encountered them
                if not crnt in IPA_CHRONEMES:
                    phone = Phone(crnt, is_long_sound)
                    sounds.append(phone)

            # If we found a syllable mark, or the transcription ended, then we know
            # that the previous syllable ends here. Thus, add all the sounds we've
            # encountered so far to it, and prepare for a new syllable. NOTE: if
            # we've encountered the end, then processing ends anyways
            if crnt in IPA_SYLLABLES or i == len(chars) - 1:
                if len(sounds) != 0:
                    syllable = Syllable(stress, sounds)
                    syllables.append(syllable)
                stress = crnt
                sounds = []

        return syllables

WordPair = tuple[Word, Word]

### Helper functions ###

def parse_ipa_characters(ipa: str) -> list[str]:
    """ Given an IPA transliteration, return all the IPA characters in it """
    # Remove any any forward slashes, square brackets or round parentheses that
    # may be used to indicate the type of pronunciation (rough, precise or
    # imprecise respectively)
    chars = re.sub(r"[\\/\[\]\(\)]", "", ipa)
    # Some scripts use `ː` to denote vowel length, some use `:`. Don't be
    # fooled: they're not the same character! We use `ː`.
    chars = chars.replace(":", "ː")

    IPA_CHARACTERS = IPA_SOUNDS + IPA_CHRONEMES + IPA_SYLLABLES
    chars = re.split("((?:" + '|'.join(IPA_CHARACTERS) # unicode IPA characters
                            + "abcdefghijklmnopqrstuvxyz" # any other alphabet character
                            + ")"
                            # they may be folllowed by a diacritic character
                            + "["
                            + ''.join(IPA_DIACRITICS)
                            + "]?)", chars)

    return [process_transliteration(ch) for ch in chars if ch != ""]

def process_transliteration(sound: str) -> str:
    """
    Return the given sound, except, if it's badly transliterated, modify
    it
    """
    if sound in BAD_TRANSLITERATIONS:
        # evil unicode hack
        sound = sound[0] + 't͡ɕ'[1] + sound[1]
    return sound

def peek(xs: list):
    """
    Return the second element in the list if that index exists, otherwise empty
    string
    """
    if len(xs) <= 1:
        return ""
    else:
        return xs[1]

### CONSTANTS ###

"""
The list of unicode characters that denote sounds in IPA text
"""
IPA_SOUNDS = [
    # Consonants
    't͡ɕ', 'tɕ',
    't͡ʂ', 'tʂ',
    't͡s', 'ts',
    't͡ʃ', 'tʃ',
    'd͡ʐ', 'dʐ',
    'd͡ʑ', 'dʑ',
    'd͡z', 'dz',
    'd͡ʒ', 'dʒ',
    'ʂ',
    'ɕ',
    'ɲ',
    'ŋ',
    'ʐ',
    'ʑ',
    'ś',
    'ɡ',
    'ʁ',
    'ʃ',
    'ʒ',
    'ɟ',
    'ɫ',
    'ʎ',
    'ç',
    'ɣ',

    'ʔ', # glottal stop

    # Oral vowels
    'ɔ',
    'ɛ',
    'ɪ',
    'ɨ',
    'ø',
    'ə',
    'ɑ',
    'œ',
    'æ',
    'ä'
    'ʌ',
    'ɐ',
    'ɤ',
    'ɒ',
    'ʊ',
    'ʉ',
    'ɵ',

    # Nasal vowels
    'ɑ̃',
    'ɛ̃',
    'œ̃',
    'ɔ̃',

    # Semi-vowels
    'ɥ',
]

"""
The list of unicode characters that denote syllables (and stress) in IPA text
"""
IPA_SYLLABLES = [
    '.',
    'ˈ',
    'ˌ',
]

"""
The list of unicode characters that denote sound length in IPA text
"""
IPA_CHRONEMES = [
    'ː',
]

"""
A(n) (incomplete) list of unicode characters used as diacritics in IPA transcriptions
"""
IPA_DIACRITICS = [
    # non-combining characters
    'ʰ', # aspirated
    'ˣ', # voiceless velar fricative
    'ⁿ', # nasal releaase
    'ʲ', # palatized
    'ʷ', # labialized
    'ˠ', # velarized

    # combining characters
    '̩', '̍ ̍', # syllabic consonant
    '̯', # non-syllabic vowel
]

"""
We only want to deal with transliterations of these sounds that *do* have a tie
above them. This is the proper way to represent affricates.
"""
BAD_TRANSLITERATIONS = ['tɕ', 'tʂ', 'ts', 'tʃ', 'dʐ', 'dʑ', 'dz', 'dʒ']
