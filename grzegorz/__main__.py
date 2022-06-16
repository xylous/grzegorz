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
from .fetcher import fetchipa
from .generator import generate
from .anki_integration import makedeck

# Why does it have to be this complicated?
def create_argparser():
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')
    # 'fetchipa' subcommand
    parser_fetchpron = subparsers.add_parser('fetchipa',
            help='Fetch all IPA pronunciations for the words into a JSON file')
    parser_fetchpron.add_argument('language',
            type=str,
            help="the language you want pronunciation for")
    parser_fetchpron.add_argument('infile',
            type=str,
            help='file containing the list of words')
    parser_fetchpron.add_argument('outfile',
            type=str,
            help='output file (JSON)')
    # 'generate' subcommand
    parser_createpairs = subparsers.add_parser('generate',
            help='Create minimal pairs, given a JSON input file')
    parser_createpairs.add_argument('infile',
            type=str,
            help='JSON file created by fetchipa')
    parser_createpairs.add_argument('outfile',
            type=str,
            help='path where the created minimal pairs will be stored')
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
    # 'makedeck' subcommand
    parser_createpairs = subparsers.add_parser('makedeck',
            help='Create an Anki deck package containing all minimal pairs')
    parser_createpairs.add_argument('infile',
            type=str,
            help="Output file of 'generate'")
    return parser

def main():
    parser = create_argparser()
    args = parser.parse_args()

    try:
        cmd = args.subparser_name
        infile = args.infile
    except:
        parser.print_help()
        return

    match cmd:
        case 'fetchipa':
            outfile = args.outfile
            language = args.language
            if not language:
                print('Invalid language')
                return
            fetchipa(infile, outfile, language)
        case 'generate':
            outfile = args.outfile
            nooptimise = args.nooptimise;
            ignore_stress = args.ignore_stress;
            generate(infile, outfile, nooptimise, ignore_stress)
        case 'makedeck':
            makedeck(infile)

main()
