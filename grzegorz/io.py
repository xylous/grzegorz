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

from grzegorz.word import (Word, WordPair)

from typing import Callable, TypeVar

T = TypeVar('T')

def readfile(path: str) -> str:
    """Return the contents of a file"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def writefile(path: str, text: str) -> None:
    """Write `text` to the given path"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


# JSON has several disadvantages, alongside being too verbose for our purposes.
# Running multiple threads, like `fetchipa()` does, would make it tricky to
# add new data to the file. On the other hand, using plain text and a thread
# mutex allows us to directly append new lines.

GRZEGORZ_WORD_FORMAT_SEPARATOR = ", "
GRZEGORZ_MINPAIR_FORMAT_SEPARATOR = " -- "

def encode_word(word: Word) -> str:
    return word.text + GRZEGORZ_WORD_FORMAT_SEPARATOR + word.ipa

def encode_minpair(pair: WordPair) -> str:
    return encode_word(pair[0]) + GRZEGORZ_MINPAIR_FORMAT_SEPARATOR + encode_word(pair[1])

def decode_word(s: str) -> Word:
    spl = s.split(GRZEGORZ_WORD_FORMAT_SEPARATOR)
    return Word(spl[0], spl[1])

def decode_minpair(s: str) -> WordPair:
    spl = s.split(GRZEGORZ_MINPAIR_FORMAT_SEPARATOR)
    return (decode_word(spl[0]), decode_word(spl[1]))

def encode_format(hook: Callable[[T], str], input: list[T]) -> str:
    return "\n".join([hook(elem) for elem in input])

def decode_format(hook: Callable[[str], T], input: str) -> list[T]:
    return [hook(line) for line in input.splitlines()]
