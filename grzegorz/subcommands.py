# Copyright (c) 2023 xylous <xylous.e@gmail.com>
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

from grzegorz.fetcher import get_ipa_for_word
from grzegorz.generator import (MinPairGenerator)
from grzegorz.anki_integration import (minpairs_to_deck, export_deck)
from grzegorz.wordlist import (wordlist, print_languages_list, valid_lang)
from grzegorz.word import Word
from grzegorz.io import *

from os import (remove, linesep)
from multiprocessing import Pool
from threading import Lock
from functools import partial
from tqdm import tqdm

def fullmake(language: str, bounds: str, clean: bool) -> None:
    """
    Practically: wrap all commands into one. If `clean` is True, then
    temporary files created by this function are removed.
    """

    wordlist_file = language + "-wordlist.txt"
    ipa_file = language + "-ipa.txt"
    minpairs_file = language + "-minpairs.txt"
    makedeck_file = "grzegorz-" + language + "-minpairs.apkg"

    if wordlist_command(language, bounds, wordlist_file) == 1:
        exit(1)
    fetchipa(wordlist_file, ipa_file, False, 20)
    generate_command(ipa_file, minpairs_file, False, False, False, False)
    makedeck(minpairs_file, makedeck_file)

    if clean:
        print("Removing temporary files...")
        remove(wordlist_file)
        remove(ipa_file)
        remove(minpairs_file)

def list_languages() -> None:
    print_languages_list()

def print_analysis(ipa: str) -> None:
    Word("", ipa).print_human_readable()

def print_minpair_check(ipa1: str, ipa2: str) -> None:
    word1 = Word("", ipa2)
    word2 = Word("", ipa1)
    generator = MinPairGenerator(False, True, True, True)
    if not generator.print_human_readable_check(word1, word2):
        exit(1)

def wordlist_command(language: str, bounds: str, outfile: str) -> int:
    """
    Fetch a word list of `numwords` and put it into `outfile` for the given
    language, if it's valid
    If the operation failed, then return 1, otherwise return 0
    """
    spl = bounds.split(":")
    if bounds.isnumeric():
        lowerbound = 0
        upperbound = int(bounds)
    elif spl[0].isnumeric() and spl[1].isnumeric():
        lowerbound = int(spl[0])
        upperbound = int(spl[1])
    else:
        print("Error: can't recognise bounds. Only positive integers are allowed before and after the ':'")
        return 1

    if lowerbound > upperbound:
        print("Error: lower bound is bigger than upper bound; abort")
        return 1

    if not valid_lang(language):
        print(language, "Error: that is not a language for which a wordlist can be fetched", sep='')
        return 1

    raw_words = wordlist(language, upperbound, lowerbound)
    if raw_words:
        writefile(outfile, '\n'.join(raw_words))
        print("Fetched", upperbound - lowerbound, language, "words into", outfile)
        return 0
    else:
        return 1

def fetchipa(infile: str, outfile: str, keep_failed: bool, numproc: int = 20) -> None:
    """
    Given an input file containing a list of words separated, fetch the IPAs and
    create a text file with their IPA spellings matched to their text
    """

    # Ensure that we're processing the data with at least one thread
    if numproc < 1:
        numproc = 1

    wordlist = readfile(infile).splitlines()

    language = wordlist.pop(0)
    words = [line for line in wordlist if line]
    numwords = len(words)

    print("NOTE:",
            "  Words are appended progressively to the file, so progress won't be lost.",
            "  However, you won't be able to read the file while the program is running.",
            sep=linesep)

    print("Fetching IPA spellings for", numwords, language, "words...")
    with open(outfile, "a", encoding='utf-8') as handle:
        with Pool(numproc) as p:
            for fetched_word in tqdm(p.imap_unordered(partial(get_ipa_for_word, language=language),
                words), total=numwords):
                if keep_failed or fetched_word.ipa != "":
                    encoded = encode_word(fetched_word) + "\n"
                    with Lock():
                        handle.write(encoded)

def generate_command(infile, outfile, nooptimise, no_phonemes, no_chronemes,
                     no_stress, filter_file_path=None) -> None:
    words = decode_format(decode_word, readfile(infile))
    g = MinPairGenerator(
        not nooptimise,
        not no_phonemes,
        not no_chronemes,
        not no_stress
    )
    if filter_file_path is not None:
        g.set_filter_pairs_from_file(filter_file_path)

    if no_phonemes and not no_chronemes and not no_stress:
        print("Generator: skipping all contrasts means no minimal pairs will be generated; abort")
        return
    if no_phonemes:
        print("Generator: phoneme contrasts will be ignored")
    if no_chronemes:
        print("Generator: chroneme contrasts will be ignored")
    if no_stress:
        print("Generator: syllable stress contrasts will be ignored")

    print('Generating minimal pairs from:', len(words), 'words')
    minpairs = g.generate(words, False)
    writefile(outfile, encode_format(encode_minpair, minpairs))
    print('Done! Generated', len(minpairs), 'minimal pairs')

def makedeck(infile: str, outfile: str) -> None:
    """Create an Anki deck given a file full of minimal pairs"""
    minpairs = decode_format(decode_minpair, readfile(infile))
    deck = minpairs_to_deck(minpairs)
    export_deck(deck, outfile)
    print('Done! Now import', outfile, 'in your Anki')
