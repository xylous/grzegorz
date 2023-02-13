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

from word import Word, MinPair, Sound, Syllable, readfile, writefile
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
        if not pair.first.phonology or not pair.last.phonology:
            return False
        # A minimal pair is kept if it has an interesting difference.
        return ((self.keep_phonemes and has_phoneme_contrast(pair, self.optimise))
                or (self.keep_chronemes and has_chroneme_contrast(pair))
                or (self.keep_stress and has_stress_contrast(pair)))

### Helper functions ###

def has_phoneme_contrast(pair: MinPair, optimise: bool) -> bool:
    first = pair.first.phonology
    last = pair.last.phonology

    # we have to work with same number of syllables
    if len(first) != len(last):
        return False

    syl_diffs = differences(first, last)
    # abort if more (or less) than one syllable is different
    if len(syl_diffs) != 1:
        return False
    syl_diffs = syl_diffs[0]

    # get the number of phones different in the matched syllable
    phones_diffs = differences(syl_diffs[0].contents, syl_diffs[1].contents)
    if len(phones_diffs) != 1 or len(syl_diffs[0].contents) != len(syl_diffs[1].contents):
        return False

    # make sure that the differences between sounds are based on phonemes, and
    # not chronemes
    diff = phones_diffs[0]
    return diff[0].long == diff[1].long and \
            (not optimise or are_interestingly_different(diff[0], diff[1]))

def has_chroneme_contrast(pair: MinPair) -> bool:
    first = pair.first.phonology
    last = pair.last.phonology

    # we have to work with same number of syllables
    if len(first) != len(last):
        return False

    syl_diffs = differences(first, last)
    # abort if more (or less) than one syllable is different
    if len(syl_diffs) != 1:
        return False
    syl_diffs = syl_diffs[0]

    # get the number of phones different in the matched syllable
    phones_diffs = differences(syl_diffs[0].contents, syl_diffs[1].contents)
    if len(phones_diffs) != 1 or len(syl_diffs[0].contents) != len(syl_diffs[1].contents):
        return False

    # make sure that the differences between sounds is based on sound length
    diff = phones_diffs[0]
    return diff[0].long != diff[1].long and diff[0].sound == diff[1].sound

def has_stress_contrast(pair: MinPair) -> bool:
    first = pair.first.phonology
    last = pair.last.phonology

    # we have to work with same number of syllables
    if len(first) != len(last):
        return False

    syl_diffs = differences(first, last)
    # abort if more (or less) than one syllable is different
    if len(syl_diffs) != 1:
        return False
    diff = syl_diffs[0]

    return diff[0].stress != diff[1].stress \
            and diff[0].contents == diff[1].contents

def strip_stress(sounds: list[str]) -> list[str]:
    """Remove stress marks from a list of sounds"""
    return [x for x in sounds if not x in ['.', 'ˈ', 'ˌ', '̯', '']]

def word_with_delimited_ipa(word: Word) -> Word:
    """
    Return the same word, except its `sounds` property is filled with all the
    sounds of the IPA
    """
    word.phonology = parse_phonologically(word.ipa)
    return word

def differences(A: list, B: list) -> list:
    """Given two lists, return pairs of elements that differ at the same index"""
    return [(a, b) for a, b in zip(A, B) if a != b]

def are_interestingly_different(s1: Sound, s2: Sound) -> bool:
    """
    Two sounds are interestingly different if they are likely to be
    confused
    """
    for diff in INTERESTING_DIFFERENCES:
        if s1.sound in diff and s2.sound in diff \
                and s1.sound != s2.sound and s1.long == s2.long:
            return True
    return False

def parse_ipa_characters(ipa: str) -> list[str]:
    """ Given an IPA transliteration, return all the IPA characters in it """
    # Remove starting and ending '/'
    chars = ipa.replace("/", "")
    # Some scripts use `ː` to denote vowel length, some use `:`. Don't be
    # fooled: they're not the same character! We use `ː`.
    chars = chars.replace(":", "ː")
    # Also, remove the diphthong tie, as that can break things.
    chars = chars.replace('̯', '')

    # Do the actual splitting
    IPA_CHARACTERS = IPA_SOUNDS + IPA_CHRONEMES + IPA_SYLLABLES
    chars = re.split("(" + '|'.join(IPA_CHARACTERS) + "|[a-z])", chars)

    return [process_transliteration(ch) for ch in chars if ch != ""]

def parse_phonologically(ipa: str) -> list[Syllable]:
    """
    Given an IPA transliteration, parse it into a very convenient format, from a
    phonological point of view
    """
    chars = parse_ipa_characters(ipa)
    syllables = []
    stress = "." # assume the first syllable is unemphasised
    sounds = []

    # sometimes we need to skip characters, namely chronemes: the same sound
    # appearing consecutively is marked as one sound, but long in length
    skip = False
    for i in range(0, len(chars)):
        if skip:
            skip = False
            continue

        crnt = chars[i]
        next = peek(chars[i :])

        # If the current character isn't a syllable (stress) mark, then that
        # means we've encountered a sound (or a chroneme character, by accident,
        # but that's skipped). Next, figure out if the current sound is short or
        # long
        if not crnt in IPA_SYLLABLES:
            is_long_sound = False
            if next == crnt or next in IPA_CHRONEMES:
                is_long_sound = True
                skip = True
            # skip chroneme characters if we've accidentally encountered them
            if not crnt in IPA_CHRONEMES:
                s = Sound(crnt, is_long_sound)
                sounds.append(s)

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

def peek(xs: list):
    """
    Return the second element in the list if that index exists, otherwise empty
    string
    """
    if len(xs) <= 1:
        return ""
    else:
        return xs[1]

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
    # diphthong tie
    '̯',
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
