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

from grzegorz.word import *
from grzegorz.generator import *

import unittest

g = MinPairGenerator(False, True, True, True)

class GeneratorTests(unittest.TestCase):
    def test_peek_empty_list(self):
        self.assertEqual(peek([]), "")

    def test_peek_one_element(self):
        self.assertEqual(peek([1]), "")

    def test_peek_several_elements(self):
        self.assertEqual(peek(["foo", "bar", "baz"]), "bar")

    def test_sounds_parser(self):
        actual = Word("", "/barˈbaz/")
        s1 = Syllable(".", [Phone("b", False), Phone("a", False), Phone("r", False)])
        s2 = Syllable("ˈ", [Phone("b", False), Phone("a", False), Phone("z", False)])
        self.assertListEqual(actual.phonology, [s1, s2])

    def test_long_sound_on_syllable_end(self):
        expected = Syllable(".", [Phone("f", False), Phone("o", True)])
        actual = Word("", "/foː/")
        self.assertListEqual(actual.phonology, [expected])

    def test_für_german(self):
        expected = Syllable(".",[Phone("f", False), Phone("y", True), Phone("ɐ", False)])
        actual = Word("", "/fyːɐ/")
        self.assertListEqual(actual.phonology, [expected])

    def test_phoneme_contrast_r_and_m_not_optimised(self):
        w1 = Word("", "/barˈbaz/")
        w2 = Word("", "/bamˈbaz/")
        self.assertTrue(g.check_phoneme_contrast((w1, w2)))

    def test_phoneme_contrast_with_chroneme_difference(self):
        w1 = Word("", "/barˈbaz/")
        w2 = Word("", "/bar:ˈbaz/")
        self.assertFalse(g.check_phoneme_contrast((w1, w2)))

    def test_chroneme_contrast(self):
        w1 = Word("", "/barˈbaz/")
        w2 = Word("", "/bar:ˈbaz/")
        self.assertTrue(g.check_chroneme_contrast((w1, w2)))

    def test_chroneme_contrast_two_diffs(self):
        w1 = Word("", "/barˈbaz/")
        w2 = Word("", "/bar:ˈba:z/")
        self.assertTrue(g.check_chroneme_contrast((w1, w2)))

    def test_syllable_stress_contrast_two_syllable(self):
        w1 = Word("", "/barˈbaz/")
        w2 = Word("", "/bar.baz/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

    def test_syllable_stress_contrast_three_syllables_1(self):
        w1 = Word("", "/barˈbaz.do/")
        w2 = Word("", "/bar.baz.do/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

    def test_syllable_stress_contrast_three_syllables_2(self):
        w1 = Word("", "/barˈbaz.do/")
        w2 = Word("", "/bar.bazˈdo/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

    def test_syllable_stress_contrast_three_syllables_3(self):
        w1 = Word("", "/barˈbaz.do/")
        w2 = Word("", "/barˌbazˈdo/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

    def test_syllable_stress_contrast_three_syllables_4(self):
        w1 = Word("", "/bar.baz.do/")
        w2 = Word("", "/barˌbazˈdo/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

    def test_syllable_stress_contrast_four_syllables_1(self):
        w1 = Word("", "/bar.baz.do.man/")
        w2 = Word("", "/barˌbazˈdo.man/")
        self.assertTrue(g.check_stress_contrast((w1, w2)))

if __name__ == '__main__':
    unittest.main()
