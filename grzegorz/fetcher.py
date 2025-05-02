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

import requests
from bs4 import BeautifulSoup
import re

### HELPER FUNCTIONS ###

def get_ipa_for_word(word: str, language: str) -> Word:
    """
    Look for the IPA transliteration of the given word in the specified language
    and return a `Word` binding it to the letters. If no transcription was
    found, then the `ipa` field of the result is empty.
    """
    language = language.capitalize()
    url = f"https://en.wiktionary.org/wiki/{word}"
    webpage = requests.get(url)
    soup= BeautifulSoup(webpage.text, "html.parser")
    pronunciations= soup.select(f'li:has(sup:has(a[href="/wiki/Appendix:{language}_pronunciation"]))' )

    ipa = ""
    # maybe blindly choosing the first IPA transliteration is not the wisest
    # choice in the world?
    if len(pronunciations):
        first_entry = pronunciations[0].find("span", {"class": "IPA"})
        if first_entry is not None:
            ipa = first_entry.text

    return Word(word, ipa)

def first_ipa_pronunciation(ipa_str: str) -> str:
    """Find the first IPA spelling in the given string"""
    result = re.findall(r"[/\[].*?[/\]]", ipa_str)
    return result[0] if len(result) else ""
