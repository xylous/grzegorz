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

from .word import Word, readfile, writefile
from multiprocessing import Pool
from functools import partial
import json
from tqdm import tqdm

# Given an input file containing a list of words separated
def fetchipa(infile, outfile):
    numproc = 20

    contents = readfile(infile).splitlines()
    language = contents.pop(0)
    words = input_to_words(contents)
    wds = []
    numwords = len(words)

    print("Fetching IPA spellings for", numwords, language, "words...")
    if numwords > 500:
        print("If you cancel, all progress will be lost!")
    with Pool(numproc) as p:
        for x in tqdm(p.imap_unordered(partial(Word.get_ipa, language=language),
            words), total=numwords):
            wds.append(x)

    jsonlog = json.dumps([word.__dict__ for word in wds])
    writefile(outfile, jsonlog)

    print('Done!')

# Turn the read input into a list of `Word`s
def input_to_words(strs):
    # Remove empty lines
    words = [Word(x, '') for x in strs if x]
    return words
