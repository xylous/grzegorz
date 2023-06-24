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

from grzegorz.word import Word, readfile, writefile

from wiktionaryparser import WiktionaryParser
from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm import tqdm
import json
import re

def fetchipa(infile: str, outfile: str) -> None:
    """
    Given an input file containing a list of words separated, fetch the IPAs and
    create a JSON file with their IPA spellings matched to their text
    """

    # For speed reasons, we use parallelism
    numproc = 10 * cpu_count()

    contents = readfile(infile).splitlines()
    language = contents.pop(0)
    words = [line for line in contents if line]
    wds = []
    numwords = len(words)

    print("Fetching IPA spellings for", numwords, language, "words...")
    if numwords > 500:
        print("If you cancel, all progress will be lost!")
    with Pool(numproc) as p:
        for x in tqdm(p.imap_unordered(partial(get_ipa_for_word, language=language),
            words), total=numwords):
            wds.append(x)

    # Don't keep entries with no IPA pronunciation
    wds = [w for w in wds if w.ipa]

    jsonlog = json.dumps([Word.obj_dict(word) for word in wds])
    writefile(outfile, jsonlog)

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
