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

from .word import Word, MinPair, readfile, writefile
import json
from tqdm import tqdm
from itertools import chain, combinations
import re

class MinPairGenerator:
    def __init__(
        self,
        optimise: bool,
        keep_phonemes: bool,
        keep_chronemes: bool,
        keep_stress: bool,
    ) -> None:
        self.optimise = optimise
        self.keep_phonemes = keep_phonemes
        self.keep_chronemes = keep_chronemes
        self.keep_stress = keep_stress

    def generate(self, infile: str, outfile: str) -> None:
        """
        Given the path to a file containing JSON data about serialised `Word`s, create
        a file `outfile` with all the minimal pairs found, in JSON format
        """
        jsonstr = readfile(infile)
        words = json.loads(jsonstr, object_hook=Word.from_dict)
        words = list(map(word_with_delimited_ipa, words))
        minpairs = []

        if not self.keep_phonemes and not self.keep_chronemes and not self.keep_stress:
            print("Generator: skipping all contrasts means no minimal pairs will be generated; abort")
            return
        if not self.keep_phonemes:
            print("Generator: phoneme contrasts will be ignored")
        if self.keep_chronemes:
            print("Generator: chroneme contrasts will be kept")
        if self.keep_stress:
            print("Generator: syllable stress contrasts will be kept")

        for i in tqdm(range(0,len(words))):
            for j in range(i+1,len(words)):
                pair = MinPair(words[i], words[j])
                if self.check_minpair(pair):
                    minpairs.append(pair)

        json_out = json.dumps([MinPair.obj_dict(pair) for pair in minpairs])
        writefile(outfile, json_out)
        print('Done! Generated', len(minpairs), 'minimal pairs')

    def check_minpair(self, pair: MinPair) -> bool:
        """
        Return True if the given pair is a minimal pair as per our options/rules,
        and False otherwise
        """
        # Skip empty entries
        if not pair.first.sounds or not pair.last.sounds:
            return False
        # A minimal pair is kept if it has an interesting difference.
        return ((self.keep_phonemes and has_phoneme_contrast(pair, self.optimise))
                or (self.keep_chronemes and has_chroneme_contrast(pair))
                or (self.keep_stress and has_stress_contrast(pair)))

### Helper functions ###

def has_phoneme_contrast(pair: MinPair, optimise: bool) -> bool:
    """
    A phoneme contrast occurs when the words in a pair are of equal length and
    have at least one difference. If `nooptimise` is False, then, additionally, it
    must have an interesting difference. If the above conditions are met, return
    True, otherwise False.
    """
    first = pair.first
    last = pair.last

    if len(first.sounds) != len(last.sounds):
        return False

    return (differences(first, last) == 1
            and (not optimise or is_interesting_pair(pair)))

def has_chroneme_contrast(pair: MinPair) -> bool:
    """
    A chroneme is a (theoretical) unit of sound that can distinguish the same
    sound by their duration. In other words, check if the given pair has a
    short-long sound length contrast, such as `pala` and `palla` in Italian
    """
    first = pair.first
    last = pair.last
    sounds1 = strip_stress(first.sounds)
    sounds2 = strip_stress(last.sounds)

    # Not a chroneme if they're the same length, or if the length differs by
    # more than one sound: it's not a minimal pair
    if len(sounds1) == len(sounds2) or abs(len(sounds1) - len(sounds2)) > 1:
        return False

    # Swap, as to have the longer string in sounds1
    if len(sounds2) > len(sounds1):
        sounds1, sounds2 = sounds2, sounds1

    num_same_sounds = 0
    seen_chroneme = False
    i = 0
    j = 0
    while(i < len(sounds1) and j < len(sounds2)):
        s1 = sounds1[i]
        s2 = sounds2[j]
        try:
            sn1 = sounds1[i+1]
            sn2 = sounds2[j+1]
        except IndexError:
            sn1 = ''
            sn2 = ''
        # If we encounter a `ː`, or some characters are doubled, then we've
        # encountered a chroneme
        if s1 == s2 == sn1 != sn2 or (sn1 == s2 and sn1 == 'ː'):
            seen_chroneme = True
        elif s1 != s2:
            i += 1
            num_same_sounds -= 1
        i += 1
        j += 1
        num_same_sounds += 1

    # We need the words to differ only by one single sound and to know that
    # there's a chroneme contrast between the words
    return seen_chroneme and num_same_sounds == len(sounds2)

def has_stress_contrast(pair: MinPair) -> bool:
    """
    Multiple words have almost the same IPA transcription, but the stress falls
    on different syllables.

    If the stressless sounds of both words are the same and the words' IPAs are
    different, then return True (i.e., it is a stress contrast)

    Concretely: /poˈte/ and /ˈpote/ (Greek) both get de-stressed to /pote/, and so
    they form a minimal pair based on a stress contrast
    """
    sounds1 = pair.first.sounds
    sounds2 = pair.last.sounds

    try:
        stress1 = sounds1.index("ˈ")
        stress2 = sounds2.index("ˈ")
        if (stress1 != stress2
                and strip_stress(sounds1) == strip_stress(sounds2)):
            return True
    except ValueError:
        pass

    return False

def strip_stress(sounds: list[str]) -> list[str]:
    """Remove stress marks from a list of sounds"""
    return [x for x in sounds if not x in ['.', 'ˈ', 'ˌ', '̯', '']]

def word_with_delimited_ipa(word: Word) -> Word:
    """
    Return the same word, except its `sounds` property is filled with all the
    sounds of the IPA
    """
    word.sounds = delimit_into_sounds(word.ipa)
    return word

def differences(word1: Word, word2: Word) -> int:
    """Return the number of differences between two word's sounds"""
    sound1 = word1.sounds
    sound2 = word2.sounds
    if len(sound1) != len(sound2):
        return 0
    count = sum(1 for a, b in zip(sound1, sound2) if a != b)
    return count

def are_interestingly_different(s1: str, s2: str) -> bool:
    """
    Two sounds are interestingly different if they are likely to be
    confused
    """
    for diff in INTERESTING_DIFFERENCES:
        if s1 in diff and s2 in diff and s1 != s2:
            return True
    return False

def is_interesting_pair(minpair: MinPair) -> bool:
    """
    If the given pair has an interesting difference, return True, otherwise
    False
    """
    sounds1 = minpair.first.sounds
    sounds2 = minpair.last.sounds
    for a, b in zip(sounds1, sounds2):
        if are_interestingly_different(a, b):
            return True
    return False

def delimit_into_sounds(ipa: str) -> list[str]:
    """Given the IPA pronunciaion of a word, return all the sounds in it"""
    # Remove starting and ending '/'
    sounds = ipa
    # Some scripts use `ː` to denote vowel length, some use `:`. Don't be
    # fooled: they're not the same character! We use `ː`.
    # Also: remove semivowel tie, as that can break things.
    sounds = sounds.replace(":", "ː")
    sounds = sounds.replace('̯', '')
    sounds = re.split("(" + '|'.join(IPA_CHARACTERS) + "|[a-z])", sounds)
    sounds = [process_transliteration(s) for s in sounds if s]
    return sounds

def process_transliteration(sound: str) -> str:
    """
    Return the given sound, except, if it's badly transliterated, modify
    it
    """
    if sound in BAD_TRANSLITERATIONS:
        # evil unicode hack
        sound = sound[0] + 't͡ɕ'[1] + sound[1]
    return sound

def parse_differences_chain(diffs_chain: list[str]) -> list[tuple[str]]:
    """
    Hardcoding is a bad practice. And tiresome as well. Especially when you add a
    new sound: you have to manually add so many pairs!

    Thus, we use chains of sounds: ['a', 'e', 'o'] returns the list of
    interesting differences `('a', 'e')`, `('a', 'o')`, `('e', 'o')` so
    basically all powersets of range two.
    """
    s = list(diffs_chain)
    # range(2, 2+1) returns all tuples that are exactly 2 in length - exactly
    # what we need
    pairs = chain.from_iterable(combinations(s, r) for r in range(2, 2+1))
    return list(pairs)

def flatten(lst: list[list]) -> set[list]:
    """Return the set of all elements belonging to the sublists of the list"""
    return set(chain(*lst))

### CONSTANTS ###

"""
The list of unicode characters that are used in IPA text and should be delimited
correctly
"""
IPA_CHARACTERS = [
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
    'ɡʲ',
    'xʲ',
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
    'sʲ',
    'zʲ',

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

    # Punctuation-related
    '.',
    'ˈ',
    'ˌ',
    'ː',
    '̯',
]

"""
We only want to deal with transliterations of these sounds that *don't* have a
tie above them. This is the proper way to represent affricates.
"""
BAD_TRANSLITERATIONS = ['tɕ', 'tʂ', 'ts', 'tʃ', 'dʐ', 'dʑ', 'dz', 'dʒ']

"""
All sounds in a particular chain are hard to be distinguished from each other.

Therefore, they form pairs of "interesting differences", which are used to
filter out all other "boring" minimal pairs: for example, "i" and "l" are so
far away phonetically they're easily distinguishable by anyone!
"""
INTERESTING_DIFFERENCES_CHAINS = [
    # Consonants
    ['t͡ɕ', 't͡ʂ', 't͡s', 't͡ʃ', 'd͡ʐ', 'd͡ʑ', 'd͡z', 'd͡ʒ',
        'ʂ', 'ʒ', 'ʃ', 'ɕ', 'zʲ', 'sʲ'],
    ['n', 'ɲ', 'ŋ'],
    ['v', 'f'],
    ['x', 'h', 'xʲ', 'ç'],
    ['z', 'ʑ', 'ʐ', 's', 'ś', 'ʂ'],
    ['ʎ', 'ɫ', 'l'],
    ['ɟ', 'j', 'g', 'ɡʲ', 'g'],

    # Oral vowels (and semi-vowels)
    ['ɑ', 'a', 'ɐ', 'ə', 'ʌ', 'æ'],
    ['e', 'ɛ', 'ɪ', 'æ'],
    ['ɨ', 'i', 'j', 'ɪ'],
    ['ɔ', 'o', 'ø', 'œ', 'ɵ'],
    ['ɥ', 'j'],
    ['ɥ', 'u', 'ɤ', 'y', 'w', 'ɒ', 'ʊ', 'ʉ'],
    ['i', 'e'],

    # Nasal vowels
    ['ɛ̃', 'ɛ'],
    ['ɛ̃', 'ə'],
    ['ɔ̃', 'ɔ'],
    ['œ̃', 'œ', 'ɔ'],
    ['ɛ̃', 'ɔ̃', 'œ̃', 'ɑ̃'],
]

"""Precomputed constant, to avoid hardcoding everything."""
INTERESTING_DIFFERENCES = flatten(list(
                            map(parse_differences_chain,
                                INTERESTING_DIFFERENCES_CHAINS)))
