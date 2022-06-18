# Changelog

## v0.3.3 - 2022-06-18

- fix: add the proper tie character to IPAs
- fix: look only for IPAs when fetching from Wiktionary; ignore rhymes

## v0.3.2 - 2022-06-17

- fix crash when fetching IPA for certain words
- fix: remove transcription marks ('/', '[' and ']') from IPA spellings when
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
