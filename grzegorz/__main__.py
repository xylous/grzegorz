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

import argparse
from .fetcher import fetchpron
from .generator import createpairs
from .anki_integration import ankideck

# Why does it have to be this complicated?
def create_argparser():
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')
    # 'fetchpron' subcommand
    parser_fetchpron = subparsers.add_parser('fetchpron',
            help='Fetch all IPA pronunciations for the words into a JSON file')
    parser_fetchpron.add_argument('language',
            type=str,
            help="the language you want pronunciation for")
    parser_fetchpron.add_argument('input',
            type=str,
            help='file containing the list of words')
    parser_fetchpron.add_argument('output',
            type=str,
            help='file containing the list of words')
    # 'createpairs' subcommand
    parser_createpairs = subparsers.add_parser('createpairs',
            help='Create minimal pairs, given a JSON input file')
    parser_createpairs.add_argument('input',
            type=str,
            help='JSON file created by fetchpron')
    parser_createpairs.add_argument('output',
            type=str,
            help='JSON file created by fetchpron')
    parser_createpairs.add_argument('--no-optimise',
            action='store_true',
            default=False,
            dest="nooptimise",
            help="generate all possible minimal pairs (default: optimise)")
    parser_createpairs.add_argument('--ignore-stress',
            action='store_true',
            default=False,
            dest="ignore_stress",
            help="ignore syllable stress in IPA text (default: don't)")
    parser_createpairs = subparsers.add_parser('ankideck',
            help='Create an Anki deck package containing all minimal pairs, WITHOUT audio')
    parser_createpairs.add_argument('input',
            type=str,
            help="Output file of 'createpairs'")
    return parser

def main():
    parser = create_argparser()
    args = parser.parse_args()

    try:
        cmd = args.subparser_name
        infile = args.input
    except:
        parser.print_help()
        return

    match cmd:
        case 'fetchpron':
            outfile = args.output
            language = args.language
            if not language:
                print('Invalid language')
                return
            fetchpron(infile, outfile, language)
        case 'createpairs':
            outfile = args.output
            nooptimise = args.nooptimise;
            ignore_stress = args.ignore_stress;
            createpairs(infile, outfile, nooptimise, ignore_stress)
        case 'ankideck':
            ankideck(infile)

main()
