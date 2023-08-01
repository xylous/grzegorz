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

from grzegorz.fetcher import fetchipa
from grzegorz.generator import (MinPairGenerator)
from grzegorz.word import (Word)
from grzegorz.anki_integration import makedeck
from grzegorz.wordlist import (wordlist, print_languages_list)

from os import remove

def fullmake(language: str, numwords: int, clean: bool) -> None:
    """
    Practically: wrap all commands into one. If `clean` is True, then
    temporary files created by this function are removed.
    """
    optimise = True
    keep_phonemes = True
    keep_chronemes = True
    keep_stress = True

    wordlist_file = language + "-wordlist.txt"
    ipa_json = language + "-ipa.json"
    minpairs_file = language + "-minpairs.json"
    makedeck_file = "grzegorz-" + language + "-minpairs.apkg"

    if wordlist(language, numwords, wordlist_file) == 1:
        exit(1)
    fetchipa(wordlist_file, ipa_json, False)
    g = MinPairGenerator(
        optimise,
        keep_phonemes,
        keep_chronemes,
        keep_stress,
    )
    g.generate(ipa_json, minpairs_file)
    makedeck(minpairs_file, makedeck_file)

    if clean:
        print("Removing temporary files...")
        remove(wordlist_file)
        remove(ipa_json)
        remove(minpairs_file)

