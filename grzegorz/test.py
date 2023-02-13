# Copyright (c) 2023 xylous <xylous.e@gmail.com>
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

from generator import *
import unittest

class GeneratorTests(unittest.TestCase):
    def test_peek_empty_list(self):
        self.assertEqual(peek([]), "")

    def test_peek_one_element(self):
        self.assertEqual(peek([1]), "")

    def test_peek_several_elements(self):
        self.assertEqual(peek(["foo", "bar", "baz"]), "bar")

    def test_sounds_parser(self):
        sounds = parse_phonologically("/barˈbaz/")
        s1 = Syllable(".", [Sound("b", False), Sound("a", False), Sound("r", False)])
        s2 = Syllable("ˈ", [Sound("b", False), Sound("a", False), Sound("z", False)])
        self.assertListEqual(sounds, [s1, s2])

if __name__ == '__main__':
    unittest.main()
