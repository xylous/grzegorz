import argparse
from .fetcher import fetchpron
from .generator import createpairs

# Why does it have to be this complicated?
def create_argparser():
    parser = argparse.ArgumentParser(
            prog='grzegorz',
            description='Generate minimal pairs from a list of words')
    subparsers = parser.add_subparsers(dest='subparser_name')
    # 'fetchpron' subcommand
    parser_fetchpron = subparsers.add_parser('fetchpron',
            help='Fetch all IPA pronunciations for the words into a JSON file')
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
    return parser

def main():
    parser = create_argparser()
    args = parser.parse_args()

    try:
        cmd = args.subparser_name
        infile = args.input
        outfile = args.output
    except:
        parser.print_help()
        return

    nooptimise = args.nooptimise;
    ignore_stress = args.ignore_stress;

    match cmd:
        case 'fetchpron':
            fetchpron(infile, outfile)
        case 'createpairs':
            createpairs(infile, outfile, nooptimise, ignore_stress)

main()
