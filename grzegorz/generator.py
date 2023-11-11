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

from grzegorz.word import (Word, WordPair,
                           PHONEME_MINPAIR, CHRONEME_MINPAIR, STRESS_MINPAIR,
                           NOT_MINPAIR)
from grzegorz.io import readfile

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
        # used for phonemes only; maybe rename?
        self.filter_pairs = DEFAULT_FILTER_PAIRS
        self.keep_phonemes = keep_phonemes
        self.keep_chronemes = keep_chronemes
        self.keep_stress = keep_stress

    def set_filter_pairs_from_file(self, path: str) -> None:
        """NOTE: the file must have comma-separated values, with the phones that
        form chains together on the same line"""
        contents = readfile(path).split("\n")
        lists_of_phonemes = []
        for line in contents:
            if line != "":
                lists_of_phonemes.append(line.replace(" ", "").split(","))
        self.filter_pairs = phoneme_lists_to_phoneme_pairs(lists_of_phonemes)

    def generate(self, words: list[Word], silent: bool = True) -> list[WordPair]:
        """
        Generate minimal pairs from the given parameters
        """
        minpairs = []

        progress_bar = tqdm(total=int(len(words) * (len(words) - 1) / 2), disable=silent)
        for i in range(0, len(words)):
            words_after = range(i+1, len(words))
            for j in words_after:
                pair = (words[i], words[j])
                if self.check_minpair(pair):
                    minpairs.append(pair)
            progress_bar.update(len(words_after))
        progress_bar.close()

        return minpairs

    def check_minpair(self, pair: WordPair) -> int:
        """
        If the given pair is not a minpair, return NOT_MINPAIR; otherwise,
        return, per case, PHONEME_MINPAIR, CHRONEME_MINPAIR or STRESS_MINPAIR
        """
        # Skip empty entries
        if not pair[0].phonology or not pair[1].phonology:
            return False
        # A minimal pair is kept if it has an interesting difference.
        if self.keep_phonemes and self.check_phoneme_contrast(pair):
            return PHONEME_MINPAIR
        elif self.keep_chronemes and self.check_chroneme_contrast(pair):
            return CHRONEME_MINPAIR
        elif self.keep_stress and self.check_stress_contrast(pair):
            return STRESS_MINPAIR
        else:
            return NOT_MINPAIR

    def check_optimised_phone_pair(self, s1: str, s2: str) -> bool:
        """
        Two sounds are interestingly different if they are likely to be confused
        """
        for diff in self.filter_pairs:
            if s1 in diff and s2 in diff and s1 != s2:
                return True
        return False

    def print_human_readable_check(self, word1: Word, word2: Word) -> int:
        word1.print_human_readable()
        print("")
        word2.print_human_readable()
        print("")
        verdict = self.check_minpair((word1, word2))
        if verdict == PHONEME_MINPAIR:
            print("minimal pair based on phoneme difference")
        elif verdict == CHRONEME_MINPAIR:
            print("minimal pair based on chroneme difference")
        elif verdict == STRESS_MINPAIR:
            print("minimal pair based on syllable stress difference")
        else:
            print("not minimal pair")
        return verdict

    def check_phoneme_contrast(self, pair: WordPair) -> bool:
        """Check if the two Words form a minimal pair based on a phoneme
        difference"""
        first = pair[0].phonology
        last = pair[1].phonology

        # we have to work with same number of syllables
        if len(first) != len(last):
            return False

        diffs = []
        for i in range(0, len(first)):
            syl1 = first[i].contents
            syl2 = last[i].contents
            if len(syl1) != len(syl2):
                return False
            for j in range(0, len(syl1)):
                if syl1[j].sound != syl2[j].sound:
                    diffs.append((syl1[j].sound, syl2[j].sound))

        if len(diffs) != 1:
            return False

        return (not self.optimise or self.check_optimised_phone_pair(diffs[0][0], diffs[0][1]))

    def check_chroneme_contrast(self, pair: WordPair) -> bool:
        """Check if the two `Word`s form a minimal pair based on a sound length
        difference (i.e. a different chroneme)"""
        first = pair[0].phonology
        last = pair[1].phonology

        # we have to work with same number of syllables
        if len(first) != len(last):
            return False

        # find the number of chroneme differences; if, at any point, we
        # encounter a differnt sound, then we know the words are too different
        # apart, and so return False
        chroneme_diffs = 0
        for i in range(0, len(first)):
            syl1 = first[i].contents
            syl2 = last[i].contents
            if len(syl1) != len(syl2):
                return False
            for j in range(0, len(syl1)):
                if syl1[j].sound != syl2[j].sound:
                    return False
                elif syl1[j].long != syl2[j].long:
                    chroneme_diffs += 1

        return chroneme_diffs >= 1

    def check_stress_contrast(self, pair: WordPair) -> bool:
        """Check if the two `Word`s form a minimal pair based on different
        placcing of syllable stress, all sounds being the same"""
        first = pair[0].phonology
        last = pair[1].phonology

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

def flatten(lst: list[list]) -> set[list]:
    """Return the set of all elements belonging to the sublists of the list"""
    return set(chain(*lst))

def phoneme_list_to_pairs(phoneme_list: list[str]) -> list[tuple[str]]:
    """
    Hardcoding is a bad practice. And tiresome as well. Especially when you add a
    new sound: you have to manually add so many pairs!

    Thus, we use lists of phonemes to group similar sounds together. For
    example, ['a', 'e', 'o'] gets turned into the following pairs of phonemes:
    `('a', 'e')`, `('a', 'o')`, `('e', 'o')`. Practically, this functions
    returns  all powersets of range two.
    """
    s = list(phoneme_list)
    # range(2, 2+1) returns all tuples that are exactly 2 in length - exactly
    # what we need
    pairs = chain.from_iterable(combinations(s, r) for r in range(2, 2+1))
    return list(pairs)

def phoneme_lists_to_phoneme_pairs(phoneme_lists: list[list[str]]) -> set[list]:
    """
    Given a list of lists of phonemes, return the combined set of all phoneme
    pairs made from every individual list.
    """
    return flatten([phoneme_list_to_pairs(list) for list in phoneme_lists])

### CONSTANTS ###

"""
All sounds in a particular chain are hard to be distinguished from each other.

Therefore, they form pairs of "interesting differences", which are used to
filter out all other "boring" minimal pairs: for example, "i" and "l" are so
far away phonetically they're easily distinguishable by anyone!
"""
DEFAULT_FILTER_PAIRS_PHONEME_LISTS = [
    # Consonants
    ['t͡ɕ', 't͡ʂ', 't͡s', 't͡ʃ', 'd͡ʐ', 'd͡ʑ', 'd͡z', 'd͡ʒ',
        'ʂ', 'ʒ', 'ʃ', 'ɕ', 'zʲ', 'sʲ'],
    ['n', 'ɲ', 'ŋ'],
    ['v', 'f'],
    ['x', 'h', 'xʲ', 'ç'],
    ['z', 'ʑ', 'ʐ', 's', 'ś', 'ʂ'],
    ['ʎ', 'ɫ', 'l'],
    ['ɟ', 'j', 'g', 'ɡʲ', 'g', 'ç'],
    ['tʲ', 'tʰ', 't' ,'d', 'dʲ', 'dʰ'],
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
DEFAULT_FILTER_PAIRS = phoneme_lists_to_phoneme_pairs(DEFAULT_FILTER_PAIRS_PHONEME_LISTS)
