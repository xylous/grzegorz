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

from grzegorz.word import Word

from wiktionaryparser import WiktionaryParser
import re

### HELPER FUNCTIONS ###

def get_ipa_for_word(word: str, language: str) -> Word:
    """
    Look on the English Wiktionary for the IPA of the given word
    """
    parser = WiktionaryParser()
    parser.set_default_language(language)
    ipa = ""
    # If we get no result, skip.
    try:
        ipa = first_ipa_pronunciation(parser.fetch(word)[0]['pronunciations']['text'][0])
        # Not all words have their IPAs on wiktionary, but they might have a
        # "Rhymes" section (try German wordlists). If we did fetch a rhyme,
        # don't add it as a valid IPA
        if ipa[0] == '-':
            ipa = ""
    except (IndexError, AttributeError, KeyError) as _:
        pass

    return Word(word, ipa)

def first_ipa_pronunciation(ipa_str: str) -> str:
    """Find the first IPA spelling in the given string"""
    return re.findall(r"[/\[].*?[/\]]", ipa_str)[0]
