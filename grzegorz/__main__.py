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

from grzegorz.fetcher import fetchipa
from grzegorz.generator import (MinPairGenerator)
from grzegorz.word import (Word)
from grzegorz.anki_integration import makedeck
from grzegorz.wordlist import (wordlist, print_languages_list)

from os import remove
import argparse

# Why does it have to be this complicated?
def create_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # 'analyse' subcommand
    parser_analyse = subparsers.add_parser('analyse',
            help='Print the result of phonologically parsing of the given IPA transcription')
    parser_analyse.add_argument('ipa',
            type=str,
            help="IPA transcription")

    # 'check' subcommand
    parser_check = subparsers.add_parser('check',
            help='Check if the two given IPAs can form minimal pair')
    parser_check .add_argument('ipa_first',
            type=str,
            help="first IPA transcription")
    parser_check .add_argument('ipa_second',
            type=str,
            help="second IPA transcription")

    # 'list-languages' subcommand
    subparsers.add_parser('list-languages',
            help='List all languages for which you can fetch a wordlist')

    # 'fullmake' command
    parser_fullmake = subparsers.add_parser('fullmake',
            help='Build an Anki deck for a language automatically')
    parser_fullmake.add_argument('language',
            type=str)
    parser_fullmake.add_argument('numwords',
            type=int,
            help='number of words to sample')
    parser_fullmake.add_argument('--clean',
            dest='clean',
            action='store_true',
            default=False,
            help='remove temporary files after building the deck')

    # 'wordlist' command
    parser_wordlist = subparsers.add_parser('wordlist',
            help='Fetch the word list for a given language, containing a certain number of words')
    parser_wordlist.add_argument('language',
            type=str,
            help='language of the wordlist')
    parser_wordlist.add_argument('numwords',
            type=int,
            help='number of words to keep')
    parser_wordlist.add_argument('outfile',
            type=str,
            help='path where the wordlist should be stored')

    # 'fetchipa' subcommand
    parser_fetchipa = subparsers.add_parser('fetchipa',
            help='Fetch all IPA pronunciations for the words into a JSON file')
    parser_fetchipa.add_argument('infile',
            type=str,
            help='file containing the list of words')
    parser_fetchipa.add_argument('outfile',
            type=str,
            help='output file (JSON)')
    parser_fetchipa.add_argument('--keep-failed',
            dest='keep_failed',
            action='store_true',
            default=False,
            help='Save the words for which no IPA was found in the output file (default: don\'t)')

    # 'generate' subcommand
    parser_generate = subparsers.add_parser('generate',
            help='Create minimal pairs, given a JSON input file')
    parser_generate.add_argument('infile',
            type=str,
            help='JSON file created by fetchipa')
    parser_generate.add_argument('outfile',
            type=str,
            help='path where the created minimal pairs will be stored')
    parser_generate.add_argument('--no-optimise',
            action='store_true',
            default=False,
            dest="nooptimise",
            help="generate all possible minimal pairs (default: optimise)")
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
            help="path to the file whose contents determine the phones to keep when optimising")

    # 'makedeck' subcommand
    parser_makedeck = subparsers.add_parser('makedeck',
            help='Create an Anki deck package containing all minimal pairs')
    parser_makedeck.add_argument('infile',
            type=str,
            help="Output file of 'generate'")
    parser_makedeck.add_argument('outfile',
            type=str,
            help="Output file; note that it should ideally have the .apkg extension")

    return parser

def fullmake(language: str, numwords: int, clean: bool) -> None:
    """
    Practically: wrap all commands into one. If `clean` is True, then
    temporary files created by this function are removed.
    """
    optimise = True
    keep_phonemes = True
    keep_chronemes = True
    keep_stress = True

    wordlist_file = language + "-wordlist.txt"
    ipa_json = language + "-ipa.json"
    minpairs_file = language + "-minpairs.json"
    makedeck_file = "grzegorz-" + language + "-minpairs.apkg"

    if wordlist(language, numwords, wordlist_file) == 1:
        exit(1)
    fetchipa(wordlist_file, ipa_json, False)
    g = MinPairGenerator(
        optimise,
        keep_phonemes,
        keep_chronemes,
        keep_stress,
    )
    g.generate(ipa_json, minpairs_file)
    makedeck(minpairs_file, makedeck_file)

    if clean:
        print("Removing temporary files...")
        remove(wordlist_file)
        remove(ipa_json)
        remove(minpairs_file)

def main() -> None:
    parser = create_argparser()
    args = parser.parse_args()

    cmd = args.subparser_name

    match cmd:
        case 'fullmake':
            clean = args.clean
            numwords = args.numwords
            language = args.language.lower()
            fullmake(language, numwords, clean)
        case 'wordlist':
            outfile = args.outfile
            numwords = args.numwords
            language = args.language.lower()
            status = wordlist(language, numwords, outfile)
            exit(status)
        case 'fetchipa':
            fetchipa(args.infile, args.outfile, args.keep_failed)
        case 'generate':
            infile = args.infile
            outfile = args.outfile
            nooptimise = args.nooptimise;
            no_phonemes = args.no_phonemes;
            no_chronemes = args.no_chronemes;
            no_stress = args.no_stress;
            filter_file_path = args.path
            g = MinPairGenerator(
                not nooptimise,
                not no_phonemes,
                not no_chronemes,
                not no_stress
            )
            if filter_file_path is not None:
                g.set_filter_pairs_from_file(filter_file_path)
            g.generate(infile, outfile)
        case 'makedeck':
            infile = args.infile
            outfile = args.outfile
            makedeck(infile, outfile)
        case 'analyse':
            Word("", args.ipa).print_human_readable()
        case 'check':
            word1 = Word("", args.ipa_first)
            word2 = Word("", args.ipa_second)
            generator = MinPairGenerator(False, True, True, True)
            if not generator.print_human_readable_check(word1, word2):
                exit(1)
        case 'list-languages':
            print_languages_list()
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
