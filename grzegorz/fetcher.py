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

from multiprocessing import Pool, cpu_count
from functools import partial
import json
from tqdm import tqdm

def fetchipa(infile: str, outfile: str) -> None:
    """
    Given an input file containing a list of words separated, fetch the IPAs and
    create a JSON file with their IPA spellings matched to their text
    """

    # For speed reasons, we use parallelism
    numproc = 10 * cpu_count()

    contents = readfile(infile).splitlines()
    language = contents.pop(0)
    words = [Word(line, '') for line in contents if line]
    wds = []
    numwords = len(words)

    print("Fetching IPA spellings for", numwords, language, "words...")
    if numwords > 500:
        print("If you cancel, all progress will be lost!")
    with Pool(numproc) as p:
        for x in tqdm(p.imap_unordered(partial(Word.get_ipa, language=language),
            words), total=numwords):
            wds.append(x)

    # Don't keep entries with no IPA pronunciation
    wds = [w for w in wds if w.ipa]

    jsonlog = json.dumps([Word.obj_dict(word) for word in wds])
    writefile(outfile, jsonlog)
