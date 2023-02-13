# Changelog

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
