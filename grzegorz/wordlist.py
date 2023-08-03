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

import requests

VALID_LANGUAGES = [
    # Germanic languages
    ('english', 'en'),
    ('german', 'de'),
    ('norwegian', 'no'),
    ('swedish', 'sv'),
    ('danish', 'da'),
    ('dutch', 'nl'),
    # Romance languages
    ('french', 'fr'),
    ('spanish', 'es'),
    ('italian', 'it'),
    ('portugese', 'pt'),
    ('portugese-brazil', 'pt_br'),
    ('romanian', 'ro'),
    # Slavic languages
    ('polish', 'pl'),
    ('ukrainian', 'uk'),
    ('russian', 'ru'),
    ('bulgarian', 'bg'),
    ('serbian', 'se'),
    ('croatian', 'hr'),
    ('slovenian', 'sl'),
    ('czech', 'cs'),
    ('slovakian', 'sk'),
    # Finno-ugric languages
    ('hungarian', 'hu'),
    ('finnish', 'fi'),
    ('estonian', 'et'),
    # Constructed languages
    ('esperanto', 'eo'),
    # Other
    ('basque', 'eu'),
    ('albanian', 'sq'),
    ('greek', 'el'),
    ('arabic', 'ar'),
    ('georgian', 'ka'),
    ('armenian', 'hy'),
    ('persian', 'fa'),
    ('hindi', 'hi'),
    ('tamil', 'ta'),
    ('chinese', 'zh'),
    ('japanese', 'ja'),
]
"""
List of languages for which word lists can be fetched, in tuple format, with the
first element being the language full name and the second element being the
language code
"""

RESOURCES_REPO_LINK = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016'
"""All the wordlists are fetched from here"""


def wordlist(lang: str, upperbound: int, lowerbound: int = 0) -> list[str]:
    """
    Return the most common words that are between index `lowerbound` and
    `upperbound` in the given language. Note that the first element is always
    the language name. If it isn't present, then the language is invalid.
    """
    if not valid_lang(lang):
        return []

    language = lang_name(lang)
    link = wordlist_link_for_lang(lang)
    words_kept_slice = slice(lowerbound, upperbound)
    raw_words = fetch_contents(link).splitlines()[words_kept_slice]
    raw_words = [line.split()[0] for line in raw_words]
    raw_words.insert(0, language)
    return raw_words

def print_languages_list() -> None:
    for (lang, code) in sorted(VALID_LANGUAGES, key=lambda pair: pair[1]):
        print(code, ", ", lang, sep="")

### HELPER FUNCTIONS ###

def valid_lang(lang: str) -> bool:
    """Check if `wordlist()` can fetch a wordlist for the given language or
    language code"""
    for pair in VALID_LANGUAGES:
        if lang in pair:
            return True
    return False

def lang_code(lang: str) -> str:
    """Given a language, return its language code, provided it's in the
    `VALID_LANGUAGES` property"""
    for pair in VALID_LANGUAGES:
        if lang in pair:
            _, code = pair
            return code
    return ''

def lang_name(lang: str) -> str:
    """Given a language, return its language fullname, provided it's in the
    `VALID_LANGUAGES` property"""
    for pair in VALID_LANGUAGES:
        if lang in pair:
            name, _ = pair
            return name
    return ''

def wordlist_link_for_lang(lang: str):
    """Return the link to the wordlist for the given language, provided it is
    valid"""
    code = lang_code(lang)
    link = RESOURCES_REPO_LINK + "/" + code + "/" + code + "_50k.txt"
    return link

def fetch_contents(link: str):
    """Return the string containing the webpage at `link`"""
    res = requests.get(link)
    return res.text
