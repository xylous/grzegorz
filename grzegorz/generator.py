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
from functools import partial
import json
from tqdm import tqdm
from itertools import chain, combinations
import re

# Given the path to a file containing JSON data about serialised `Word`s, create
# a file `outfile` with all the minimal pairs found
def generate(
    infile: str,
    outfile: str,
    nooptimise: bool,
    ignore_stress: bool
) -> None:
    jsonstr = readfile(infile)
    words = json.loads(jsonstr, object_hook=Word.from_dict)
    words = list(map(partial(word_with_delimited_ipa, ignore_stress=ignore_stress), words))
    minpairs = []
    if ignore_stress:
        print("Okay, syllable stress will be ignored")
    # NOTE: we must first generate all possibilities and only then filter out
    # the interesting ones because the function checking for differences might
    # miss things otherwise
    print('Generating all possible minimal pairs...')
    for i in tqdm(range(0,len(words))):
        w1 = words[i]
        for j in range(i+1,len(words)):
            w2 = words[j]
            if w1.sounds == w2.sounds or len(w1.sounds) != len(w2.sounds):
                continue
            diffs = differences(w1, w2)
            if diffs == 1:
                minpairs.append(MinPair(w1, w2))
    if not nooptimise:
        print('Filtering uninteresting pairs...')
        minpairs = [x for x in map(interesting_pair, minpairs) if x]
    json_out = json.dumps([MinPair.obj_dict(pair) for pair in minpairs])
    writefile(outfile, json_out)
    print('Done! Generated', len(minpairs), 'minimal pairs')

### Helper functions ###

# Return the same word, except its IPA is delimited
def word_with_delimited_ipa(word: Word, ignore_stress: bool) -> Word:
    word.sounds = delimit_into_sounds(word.ipa, ignore_stress)
    return word

# Return the number of differences between two word's sounds
def differences(word1: Word, word2: Word) -> int:
    sound1 = word1.sounds
    sound2 = word2.sounds
    if len(sound1) != len(sound2):
        return 0
    count = sum(1 for a, b in zip(sound1, sound2) if a != b)
    return count

# Two sounds are interestingly different if they are likely to be confused
def are_interestingly_different(s1: str, s2: str) -> bool:
    for diff in INTERESTING_DIFFERENCES:
        if s1 in diff and s2 in diff and s1 != s2:
            return True
    return False

# If the given pair has an interesting difference, return it. Otherwise, return
# None
def interesting_pair(minpair: MinPair) -> MinPair|None:
    ipa1 = minpair.first.ipa
    ipa2 = minpair.last.ipa
    for a, b in zip(ipa1, ipa2):
        if are_interestingly_different(a, b):
            return minpair
    else:
        return None

# Given the IPA pronunciaion of a word, return all the sounds in it
def delimit_into_sounds(ipa: str, ignore_stress: bool) -> list[str]:
    # Remove starting and ending '/'
    sounds = ipa
    if ignore_stress:
        sounds = re.sub("[.ˈˌ]", "", sounds)
    # Some scripts use `ː` to denote vowel length, some use `:`. Don't be
    # fooled: they're not the same character! We use `ː`.
    sounds = re.sub(":", "ː", sounds)
    sounds = re.split("(" + '|'.join(IPA_CHARACTERS) + "|[a-z])[ː]?", sounds)
    sounds = [process_transliteration(s) for s in sounds if s]
    return sounds

# Return the given sound, except, if it's badly transliterated, modify it
def process_transliteration(sound: str) -> str:
    if sound in BAD_TRANSLITERATIONS:
        # evil unicode hack
        sound = sound[0] + 't͡ɕ'[1] + sound[1]
    return sound

# Hardcoding is a bad practice. And tiresome as well. Especially when you add a
# new sound: you have to manually add so many pairs!
def parse_differences_chain(diffs_chain: list[str]) -> list[tuple[str]]:
    s = list(diffs_chain)
    # range(2, 2+1) returns all tuples that are exactly 2 in length - exactly
    # what we need
    pairs = chain.from_iterable(combinations(s, r) for r in range(2, 2+1))
    return list(pairs)

# Return the set of all elements belonging to the sublists of the list
def flatten(lst: list[list]) -> set[list]:
    return set(chain(*lst))

### CONSTANTS ###

# The list of unicode characters that are used in IPA text and should be
# delimited correctly
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

    # Nasal vowels
    'ɑ̃',
    'ɛ̃',
    'œ̃',
    'ɔ̃',

    # Semi-vowels
    'ɥ',
]

# We only want to deal with transliterations of these sounds that *don't* have a
# tie above them. This is the proper way to represent affricates.
BAD_TRANSLITERATIONS = ['tɕ', 'tʂ', 'ts', 'tʃ', 'dʐ', 'dʑ', 'dz', 'dʒ']

# All sounds in a particular chain are hard to be distinguished from each other.
# Therefore, they form pairs of "interesting differences", which are used to
# filter out all other "boring" minimal pairs: for example, "i" and "l" are so
# far away phonetically they're easily distinguishable by anyone!
INTERESTING_DIFFERENCES_CHAINS = [
    # Consonants
    ['t͡ɕ', 't͡ʂ', 't͡s', 't͡ʃ', 'd͡ʐ', 'd͡ʑ', 'd͡z', 'd͡ʒ', 'ʂ', 'ʒ', 'ʃ', 'ɕ'],
    ['n', 'ɲ', 'ŋ'],
    ['v', 'f'],
    ['x', 'h', 'xʲ', 'ç'],
    ['z', 'ʑ', 'ʐ', 's', 'ś', 'ʂ'],
    ['ʎ', 'ɫ', 'l'],
    ['ɟ', 'j', 'g', 'ɡʲ', 'g'],

    # Oral vowels (and semi-vowels)
    ['ɑ', 'a', 'ɐ', 'ə', 'ʌ', 'aː', 'ɑː'],
    ['e', 'ɛ', 'e:', 'ɛː', 'ɪ', 'ɪː', 'iː'],
    ['ɨ', 'i', 'j', 'ɪ', 'ɪː'],
    ['ɔ', 'o', 'ø', 'œ', 'øː', 'oː'],
    ['ɥ', 'j'],
    ['ɥ', 'u', 'ɤ', 'y', 'w', 'uː', 'yː'],
    ['i', 'e'],
    ['ɑː', 'ɔː', 'uː', 'ɛː', 'ɪː'],

    # Nasal vowels
    ['ɛ̃', 'ɛ'],
    ['ɛ̃', 'ə'],
    ['ɔ̃', 'ɔ'],
    ['œ̃', 'œ', 'ɔ'],
    ['ɛ̃', 'ɔ̃', 'œ̃', 'ɑ̃'],
]

# Precomputed constant, to avoid hardcoding everything.
INTERESTING_DIFFERENCES = flatten(list(
                            map(parse_differences_chain,
                                INTERESTING_DIFFERENCES_CHAINS)))
