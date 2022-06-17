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
from .word import writefile

# List of languages for which word lists can be fetched
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

# This is where all the lists are fetched from
RESOURCES_REPO_LINK = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016'

# Fetch a word list of `numwords` and put it into `outfile` for the given
# language, if it's valid
# NOTE: the language name should be all lowercase
def wordlist(lang, numwords, outfile):
    language = lang_name(lang)
    if not valid_lang(lang):
        print(lang, "? I can't fetch a wordlist for that", sep='')
        return
    link = wordlist_link_for_lang(lang)
    words_kept_slice = slice(0, numwords)
    raw_words = fetch_contents(link).splitlines()[words_kept_slice]
    raw_words = list(map(format_line, raw_words))
    raw_words.insert(0, language)
    writefile(outfile, '\n'.join(raw_words))
    print("Fetched", numwords, language, "words into", outfile)
    return

### HELPER FUNCTIONS ###

# We only accept languages that are on the list
def valid_lang(lang):
    for pair in VALID_LANGUAGES:
        if lang in pair:
            return True
    return False

# Given a language, return its language code
def lang_code(lang):
    for pair in VALID_LANGUAGES:
        if lang in pair:
            _, code = pair
            return code
    return ''

# Given a language, return its language code
def lang_name(lang):
    for pair in VALID_LANGUAGES:
        if lang in pair:
            name, _ = pair
            return name
    return ''

# Return the link to the wordlist for the given language
def wordlist_link_for_lang(lang):
    code = lang_code(lang)
    link = RESOURCES_REPO_LINK + "/" + code + "/" + code + "_50k.txt"
    return link

# Return the string containing the webpage at `link`
def fetch_contents(link):
    res = requests.get(link)
    return res.text

# The format of the list we fetched is not perfect: we need to choose only the
# first word on every line
def format_line(line):
    first_word = line.split()[0]
    return first_word
