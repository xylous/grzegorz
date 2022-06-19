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
            pair = MinPair(w1, w2)
            if (has_phoneme_contrast(pair, nooptimise)
                    or has_chroneme_contrast(pair)
                    or has_stress_contrast(pair)):
                minpairs.append(pair)
    json_out = json.dumps([MinPair.obj_dict(pair) for pair in minpairs])
    writefile(outfile, json_out)
    print('Done! Generated', len(minpairs), 'minimal pairs')

### Helper functions ###

# A phoneme contrast occurs when the words in a pair are of equal length and
# have at least one difference. If `nooptimise` is False, then, additionally, it
# must have an interesting difference. If the above conditions are met, return
# True, otherwise False.
def has_phoneme_contrast(pair: MinPair, nooptimise: bool) -> bool:
    first = pair.first
    last = pair.last

    if len(first.sounds) == len(first.sounds):
        return False

    if differences(first, last) == 1:
        if nooptimise or interesting_pair(pair):
            return True
    return False

# A chroneme is a (theoretical) unit of sound that can distinguish the same
# sound by their duration. In other words, check if the given pair has a
# short-long sound length contrast, such as `pala` and `palla` in Italian
def has_chroneme_contrast(pair: MinPair) -> bool:
    first = pair.first
    last = pair.last
    if len(first.sounds) == len(last.sounds):
        return False

    len_shortest = min(len(first.sounds), len(last.sounds))
    if similarities(first, last, 1) == len_shortest:
        return True

    return False

# Count the number of similarities between two words' sounds. Every non-common
# sound is removed
def similarities(word1: Word, word2: Word, max_len_diff) -> int:
    sound1 = word1.sounds
    sound2 = word2.sounds
    count = 0

    # Always assume sound1 is longer than sound2
    if len(sound2) > len(sound1):
        tmp = sound1
        sound1 = sound2
        sound2 = tmp

    # Skip pairs that exceed the maximum length difference
    if abs(len(sound1) - len(sound2)) > max_len_diff:
        return -1

    for i in range(0, len(sound1)):
        s1 = sound1[i]
        s2 = sound2[i]
        if s1 == s2:
            count += 1
        else:
            sound1.pop(i)

        # We might exceed the limit
        if i + 1 == len(sound1):
            break

    return count

# Multiple words might have almost the same IPA transcription, but the stress
# falls on different syllables.
#
# If the stressless sounds of both words are the same and the words' IPAs are
# different, then return True (i.e., it is a stress contrast)
#
# Concretely: /poˈte/ and /ˈpote/ (Greek) both get de-stressed to /pote/, and so
# they form a minimal pair based on a stress contrast
def has_stress_contrast(pair: MinPair) -> bool:
    sounds1 = pair.first.sounds
    sounds2 = pair.last.sounds

    if strip_stress(sounds1) == strip_stress(sounds2):
        return True

    return False

# Remove stress marks from a list of sounds
def strip_stress(sounds: list[str]) -> list[str]:
    return [x for x in sounds if not x in ['.', 'ˈ', 'ˌ']]

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
    # Some scripts use `ː` to denote vowel length, some use `:`. Don't be
    # fooled: they're not the same character! We use `ː`.
    sounds = re.sub(":", "ː", sounds)
    sounds = re.split("(" + '|'.join(IPA_CHARACTERS) + "|[a-z])[ː]?", sounds)
    sounds = [process_transliteration(s) for s in sounds if s]
    if ignore_stress:
        sounds = strip_stress(sounds)
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

    # Punctuation-related
    '.',
    'ˈ',
    'ˌ',
    'ː',
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
    ['ɑ', 'a', 'ɐ', 'ə', 'ʌ', 'aː', 'ɑː', 'æ'],
    ['e', 'ɛ', 'e:', 'ɛː', 'ɪ', 'ɪː', 'iː', 'æ'],
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
