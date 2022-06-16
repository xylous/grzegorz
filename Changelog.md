# Changelog

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
