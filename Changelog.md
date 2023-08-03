# Changelog

## v0.6.0 - 2023-08-03

- improve `wordlist`: accept ranges, e.g. `3000:5000`, which returns only the
    3000th up to the 5000th most common words
- add `--numproc` option to `fetchipa`, to explicitly set the number of
    concurrent processes that should handle the wordlist
- fix Anki flashcard template: highlight the correct word in Card 1, as it is
    highlighted in Card 2
- optimise `fetchipa` by removing time-expensive code
- change: replace JSON with a custom place-text format
- change: make `fetchipa` not lose progress whenever it is cancelled, by writing
    (appending) progressively to the output file

## v0.5.0 - 2023-06-29

- add diacritics parsing
- add `analyse` command, for phonologically analysing a given IPA transcription
- add `check` command, for determining whether two IPA transcriptions form a
    minimal pair
- add `list-languages` command, for printing out all languages (and their codes)
    for which a wordlist can be fetched
- add `--keep-failed` option to `fetchipa`
- add `--filter-file` (`-f`) option to `generate`; this way, you can specify
    which phonemes may form a minimal pair instead of always relying on a
    default
- improve minimal pair generation performance
- fix bugs related to `fullmake` trying to generate even if the given language
    is invalid
- fix bug where long sounds at the end of a syllable would make the entire
    syllable not be registered
- fix chroneme and stress contrast checkers, which weren't very reliable for any
    words larger than one syllable
- improve phoneme contrast checker by allowing phonemes to have different
    lengths; ergo, more minimal pairs found
- change: specify the output file of the `makedeck` command instead of always
    using the same name (`grzegorz-anki-deck.apkg`)
- change: keep chroneme and stress contrasts by default during minimal pair
    generation; replace `--keep-chronemes` with `--no-chronemes` and
    `--keep-stress` with `--no-stress`
- refactor to remove redundancies + add unit tests
- completely change the documentation structure

## v0.4.10 - 2023-05-14

- fix ModuleNotFound error where `grzegorz` wouldn't run at all because import
    weren't prefixed with the module name

## v0.4.9 - 2023-02-13

- generator:
    - parse every word's IPA phonologically, delimiting it into syllables and
        sounds
    - increase performance when generating minimal pairs based on syllable
        stress and chronemes (due to the above)
    - add a few unit tests
    - fix: update relative imports, removing starting dots

## v0.4.8 - 2022-08-11

- Anki flashcards:
    - fix error that autoplayed audio on both the back and the front of the
        cards
    - change appearance of boxes containing words; use black (on light theme)
        and white (on dark theme)

## v0.4.7 - 2022-07-11

- fix `AttributeError` when running `fetchipa` for e.g. Greek

## v0.4.6 - 2022-07-11

- fix `fetchipa`:
    - don't hardcode the number of parallel processes
    - fix `UnicodeEncodeError` when writing files

## v0.4.5 - 2022-07-09

- `generate`: when optimising, keep `sj` and `zj` phoneme contrasts
- refactor comments

## v0.4.4 - 2022-06-24

- `generate`:
    - add `--no-phonemes`, `--keep-chronemes`, `--keep-stress` options
    - remove `--ignore-stress` option
    - refactor code structure

## v0.4.3 - 2022-06-23

- fix: when converting a dictionary to a `Word`, add slashes around its IPA, so
    that Anki flashcards look neater
- change aspect of the Anki flashcards

## v0.4.2 - 2022-06-23

- fix: change required Python version to 3.10 so `match` is supported
- fix: use `with` statement when handling file I/O
- fix: try-except on specific errors, not any
- README:
    - add 'From source' installation instructions
    - expand the IPA abbreviation to avoid ambiguity

## v0.4.1 - 2022-06-20

- fix phoneme, chroneme and stress contrast checkers (ALL had bugs!)
- fetchipa: don't store words that have no IPA spelling

## v0.4.0 - 2022-06-19

- generator: look for phoneme, chroneme, or syllable stress-related differences
    in minimal pairs
- expand chains of phoneme differences
- parse and use `ː` character for chroneme contrasts, not phoneme contrasts

## v0.3.7 - 2022-06-19

- change `generate`: write output as JSON
- fix: use regex to find IPA when fetching them
- refactor code: add types

## v0.3.6 - 2022-06-18

- add more long vowel sounds to the generator
- add guard for running main()
- setup.cfg: export a command, `grzegorz`

## v0.3.5 - 2022-06-18

- upload project to PyPi; update installation instructions

## v0.3.4 - 2022-06-18

- fix: use `ː` instead of `:` to mark punctuation; I was misled, colons are
    *not* used in the IPA
    - fix: all possible `:` (colons) will be transformed into `ː`

## v0.3.3 - 2022-06-18

- fix: add the proper tie character to IPAs
- fix: look only for IPAs when fetching from Wiktionary; ignore rhymes

## v0.3.2 - 2022-06-17

- fix crash when fetching IPA for certain words
- fix: remove transcription marks (`/`, `[` and `]`) from IPA spellings when
    fetching them
- fix: transliterate all affricates with a tie (IPA: `'͡'`)
- refactor: precompute "interesting differences" instead of hardcoding them
- parse sounds common to the English IPA
- add "interesting differences" for sounds common to the English IPA

## v0.3.1 - 2022-06-17

- rephrase paragraphs in README as to avoid ambiguity re: the word
    'pronunciation'
- fetchipa: change the message printed to console slightly, to avoid ambiguity

## v0.3.0 - 2022-06-17

- rename subcommands
- add `wordlist`, `fullmake` commands
- fix README-related issues
- add "Importing in Anki" section to README

## v0.2.0 - 2022-06-16

- minimal pair generation:
    - delimit IPAs into sounds, as to correctly process sounds whose computer
        representation is composed of multiple letters: `d͡ʐ`, `t͡ɕ`, `xʲ` etc.
    - parse `:` after certain sounds
    - add more pairs of "interesting differences"
- add `ankideck` command to make an Anki deck with the minimal pairs, but no
    audio

## v0.1.0 - 2022-06-15

- add `fetchpron`, `createpairs` commands and options for them
- add usage information, roadmap, etc.

## v0.0.0 - 2022-06-15

- initialise project (README, LICENSE, Changelog)
