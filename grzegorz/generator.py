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

from grzegorz.word import (Word, MinPair, Phone, readfile, writefile,
                           PHONEME_MINPAIR, CHRONEME_MINPAIR, STRESS_MINPAIR,
                           NOT_MINPAIR)

import json
from tqdm import tqdm
from itertools import chain, combinations

class MinPairGenerator:
    def __init__(
        self,
        optimise: bool,
        keep_phonemes: bool,
        keep_chronemes: bool,
        keep_stress: bool,
    ) -> None:
        self.optimise = optimise
        self.optimised_phone_pairs = INTERESTING_DIFFERENCES
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

    def check_minpair(self, pair: MinPair) -> int:
        """
        If the given pair si not a minpair, return NOT_MINPAIR; otherwise,
        return, per case, PHONEME_MINPAIR, CHRONEME_MINPAIR and STRESS_MINPAIR
        """
        # Skip empty entries
        if not pair.first.phonology or not pair.last.phonology:
            return False
        # A minimal pair is kept if it has an interesting difference.
        if self.keep_phonemes and self.check_phoneme_contrast(pair, self.optimise):
            return PHONEME_MINPAIR
        elif self.keep_chronemes and self.check_chroneme_contrast(pair):
            return CHRONEME_MINPAIR
        elif self.keep_stress and self.check_stress_contrast(pair):
            return STRESS_MINPAIR
        else:
            return NOT_MINPAIR

    def check_optimised_phone_pair(self, s1: Phone, s2: Phone) -> bool:
        """
        Two sounds are interestingly different if they are likely to be confused
        """
        for diff in self.optimised_phone_pairs:
            if s1.sound in diff and s2.sound in diff \
                    and s1.sound != s2.sound and s1.long == s2.long:
                return True
        return False

    def print_human_readable_check(self, word1: Word, word2: Word) -> int:
        word1.print_human_readable()
        print("")
        word2.print_human_readable()
        print("")
        verdict = self.check_minpair(MinPair(word1, word2))
        if verdict == PHONEME_MINPAIR:
            print("minimal pair based on phoneme difference")
        elif verdict == CHRONEME_MINPAIR:
            print("minimal pair based on chroneme difference")
        elif verdict == STRESS_MINPAIR:
            print("minimal pair based on syllable stress difference")
        else:
            print("not minimal pair")
        return verdict

    def check_phoneme_contrast(self, pair: MinPair, optimise: bool) -> bool:
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
                (not optimise or self.check_optimised_phone_pair(diff[0], diff[1]))

    def check_chroneme_contrast(self, pair: MinPair) -> bool:
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

    def check_stress_contrast(self, pair: MinPair) -> bool:
        first = pair.first.phonology
        last = pair.last.phonology

        # we have to work with same number of syllables
        if len(first) != len(last):
            return False

        fst_stress = []
        snd_stress = []
        for i in range(0, len(first)):
            if first[i].contents != last[i].contents:
                return False
            fst_stress += first[i].stress
            snd_stress += last[i].stress

        return fst_stress != snd_stress

### Helper functions ###

def differences(A: list, B: list) -> list:
    """Given two lists, return pairs of elements that differ at the same index"""
    return [(a, b) for a, b in zip(A, B) if a != b]

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
    ['ɟ', 'j', 'g', 'ɡʲ', 'g', 'ç'],
    [ 'tʲ', 'tʰ', 't' ,'d', 'dʲ', 'dʰ'],
    ['r', 'ʁ'],

    # Oral vowels (and semi-vowels)
    ['ɑ', 'a', 'ɐ', 'ə', 'ʌ', 'æ', 'ä', 'ɐ̯'],
    ['ɑ', 'ə', 'œ'],
    ['e', 'ɛ', 'ɪ', 'æ'],
    ['ɨ', 'i', 'j', 'ɪ'],
    ['ɔ', 'o', 'ø', 'œ', 'ɵ'],
    ['ɥ', 'j'],
    ['ɥ', 'u', 'ɤ', 'y', 'w', 'ɒ', 'ʊ', 'ʉ', 'ʊ̯'],
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
