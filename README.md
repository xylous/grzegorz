# grzegorz

`grzegorz` is a linguistics tool which primarily concerns minimal pairs. For a
detailed history of the project's development, check the
[Changelog](./Changelog.md)

#### Overview

NOTE: throughout the documentation, "IPA" is used as an abbreviation for
[International Phonetic
Alphabet](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
transcription.

- [What are minimal pairs?](./doc/minimal-pairs.md)
- [Usage manual](./doc/USER-MANUAL.md), contains brief technical descriptions of
    everything
- [Quickshot phonological parsing](./doc/phonological-analysis.md)
- [Getting a decently-sized wordlist](./doc/wordlist.md)
- [Fetching International Phonetic Alphabet spellings](./doc/ipa-fetch.md)
- [Finding minimal pairs with the help of the generator](./doc/generator.md)
- [Creating an Anki deck and importing it into the app](./doc/anki-integration.md)
- [The convenient `fullmake` command](./doc/fullmake.md)

## Getting started

### Requirements

- python3
- pip

### Installation

Make sure the pip installation directory (default: `${HOME}/.local/bin`) is on
your `${PATH}`. If not, add it (to your `.bashrc` or `.zshrc` preferably):

```
export PATH="${HOME}/.local/bin:${PATH}"
```

#### From PyPi

```
$ pip install grzegorz
```

#### From source

Clone this repository and run pip:

```
$ git clone https://github.com/xylous/grzegorz grzegorz
$ cd grzegorz
$ pip install .
```

### Usage

Check [the "overview" section](#overview)

## Roadmap

- [x] fetch a wordlist of most used words in a given language
- [x] fetch the International Phonetic Alphabet spelling for a given wordlist
- [x] generate minimal pairs
    - [x] look for phoneme differences
        - [x] optimise: look for interesting differences
        - [x] optimise: ignore stressed syllables
    - [x] look for chroneme differences
    - [x] look for syllable stress differences
- [x] Anki integration
    - [x] create Anki flashcards from the generated minimal pairs
    - [x] export a deck containing the created flashcards
    - [ ] ~~add audio pronunciations for every flashcard~~
- [ ] print phonetical analysis of a word:
    - [x] given its IPA
    - [ ] given its language
- [x] check if two words form a minimal pair, given their IPAs
- [ ] search and print the IPA of a word in a given language (on the English
    Wiktionary)
- [ ] minimise side effects of functions, delegate commands to wrappers around
    class functions
- [ ] documentation
    - [x] technical docs for usage as a binary
    - [x] "tutorial" for usage as a binary
    - [ ] technical docs for usage as a library
    - [ ] "tutorial" for usage as a library

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

But, honestly, the greatest contribution you can make is to add International
Phonetic Alphabet (IPA) spellings to words on the [English
Wiktionary](https://en.wiktionary.org), which is the source for all the
spellings that `grzegorz` uses. The more IPA spellings there are, the higher the
number of words that can be used, the more possibilities for minimal pairs.

## License

[GPLv3](./LICENSE)
