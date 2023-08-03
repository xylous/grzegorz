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
    Look for the IPA transliteration of the given word in the specified language
    and return a `Word` binding it to the letters. If no transcription was
    found, then the `ipa` field of the result is empty.
    """
    parser = WiktionaryParser()
    parser.set_default_language(language)
    ipa = ""
    fetched = parser.fetch(word)
    if len(fetched):
        first_entry = fetched[0]
        pronunciations = first_entry.get('pronunciations')
        text = pronunciations.get('text')
        if len(text):
            ipa = first_ipa_pronunciation(text[0])
    # Not all words have their IPAs on wiktionary, but they might have a
    # "Rhymes" section (many German words do, for example). If we did fetch a
    # rhyme, don't add it as a valid IPA
    if len(ipa) and ipa[0] == '-':
        ipa = ""

    return Word(word, ipa)

def first_ipa_pronunciation(ipa_str: str) -> str:
    """Find the first IPA spelling in the given string"""
    result = re.findall(r"[/\[].*?[/\]]", ipa_str)
    return result[0] if len(result) else ""
