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

from grzegorz.subcommands import *

import argparse

# Why does it have to be this complicated?
def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # 'analyse' subcommand
    parser_analyse = subparsers.add_parser('analyse',
            help='Parse the given IPA transcription')
    parser_analyse.add_argument('ipa',
            type=str)

    # 'check' subcommand
    parser_check = subparsers.add_parser('check',
            help='Check if the two given IPAs can form a minimal pair')
    parser_check.add_argument('ipa_first',
            type=str)
    parser_check.add_argument('ipa_second',
            type=str)

    # 'list-languages' subcommand
    subparsers.add_parser('list-languages',
            help='List all languages for which you can fetch a wordlist')

    # 'fullmake' command
    parser_fullmake = subparsers.add_parser('fullmake',
            help=f'Build an Anki deck for a language (equivalent of \'wordlist\', \'fetchipa\', \'generate\', \'makedeck\')')
    parser_fullmake.add_argument('language',
            type=str)
    parser_fullmake.add_argument('bounds',
            type=str,
            help='number of words to keep, e.g. "5000"; alternatively, the range of words to keep, e.g. "1500:3000"')
    parser_fullmake.add_argument('--clean',
            dest='clean',
            action='store_true',
            default=False,
            help='remove temporary files after building the deck')

    # 'wordlist' command
    parser_wordlist = subparsers.add_parser('wordlist',
            help='Get the specified number of words from a frequency wordlist in the given language')
    parser_wordlist.add_argument('language',
            type=str,
            help='language of the wordlist')
    parser_wordlist.add_argument('bounds',
            type=str,
            help='number of words to keep, e.g. "5000"; alternatively, the range of words to keep, e.g. "1500:3000"')
    parser_wordlist.add_argument('outfile',
            type=str,
            help='path where the wordlist should be stored')

    # 'fetchipa' subcommand
    parser_fetchipa = subparsers.add_parser('fetchipa',
            help='Fetch IPA pronunciations for words in a wordlist')
    parser_fetchipa.add_argument('infile',
            type=str,
            help='wordlist output file')
    parser_fetchipa.add_argument('outfile',
            type=str)
    parser_fetchipa.add_argument('--keep-failed',
            dest='keep_failed',
            action='store_true',
            default=False,
            help='In the output file, keep the words with no found IPA (default: don\'t)')
    parser_fetchipa.add_argument('--numproc',
            type=int,
            dest='numproc',
            default=20,
            help='Number of concurrent processes to handle the wordlist; default: 20')

    # 'generate' subcommand
    parser_generate = subparsers.add_parser('generate',
            help='Find minimal pairs based on the output file of \'fetchipa\'')
    parser_generate.add_argument('infile',
            type=str,
            help='file created by fetchipa')
    parser_generate.add_argument('outfile',
            type=str,
            help='path where the created minimal pairs will be stored')
    parser_generate.add_argument('--no-optimise',
            action='store_true',
            default=False,
            dest="nooptimise",
            help="generate all possible minimal pairs (default: similar sounds)")
    parser_generate.add_argument('--no-phonemes',
            action='store_true',
            default=False,
            dest="no_phonemes",
            help="ignore minimal pairs containing a phoneme contrast")
    parser_generate.add_argument('--no-chronemes',
            action='store_true',
            default=False,
            dest="no_chronemes",
            help="ignore minimal pairs containing a chroneme contrast")
    parser_generate.add_argument('--no-stress',
            action='store_true',
            default=False,
            dest="no_stress",
            help="ignore minimal pairs with a difference in syllable stress")
    parser_generate.add_argument('-f', '--filter-file',
            type=str,
            dest="path",
            help="path to file with rules for desired phoneme differences")

    # 'makedeck' subcommand
    parser_makedeck = subparsers.add_parser('makedeck',
            help='Create an Anki deck package file from the output of the \'generate\' command')
    parser_makedeck.add_argument('infile',
            type=str,
            help="output file of 'generate'")
    parser_makedeck.add_argument('outfile',
            type=str,
            help="(.apkg extension)")

    return parser

def main() -> None:
    parser = create_argparser()
    args = parser.parse_args()

    cmd = args.subparser_name

    match cmd:
        case 'fullmake':
            clean = args.clean
            bounds = args.bounds
            language = args.language.lower()
            fullmake(language, bounds, clean)
        case 'wordlist':
            status = wordlist_command(args.language.lower(), args.bounds, args.outfile)
            exit(status)
        case 'fetchipa':
            fetchipa(args.infile, args.outfile, args.keep_failed, args.numproc)
        case 'generate':
            infile = args.infile
            outfile = args.outfile
            nooptimise = args.nooptimise;
            no_phonemes = args.no_phonemes;
            no_chronemes = args.no_chronemes;
            no_stress = args.no_stress;
            filter_file_path = args.path
            generate_command(infile, outfile, nooptimise, no_phonemes, no_chronemes,
                     no_stress, filter_file_path)
        case 'makedeck':
            makedeck(args.infile, args.outfile)
        case 'analyse':
            print_analysis(args.ipa)
        case 'check':
            print_minpair_check(args.ipa_first, args.ipa_second)
        case 'list-languages':
            list_languages()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
