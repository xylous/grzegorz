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
    'english',
    # Romance languages
    'french',
    # Slavic languages
    'polish',
]

# This is where all the lists are fetched from
RESOURCES_REPO_LINK = 'https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016'

# We only accept languages that are on the list
def valid_lang(lang):
    return lang in VALID_LANGUAGES

# Given a language, return its language code
def lang_code(lang):
    code = ''
    match lang:
        case 'english':
            code = 'en'
        case 'french':
            code = 'fr'
        case 'polish':
            code = 'pl'
    return code
