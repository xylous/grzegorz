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

def readfile(path: str) -> str:
    """Return the contents of a file"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def writefile(path: str, text: str) -> None:
    """Write `text` to the given path"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
