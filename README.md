# grzegorz

`grzegorz` is a minimal pair generator. For a detailed history of the project's
development, check the [Changelog](./Changelog.md)

Minimal pairs are pairs of words that differ only very slightly, or, as
linguists say, by one *phonological unit*, although that's just jargon. Case in
point, they can differ:

- by one sound (linguist jargon: *phoneme*) - e.g. English "bat" and "pat",
    French "rue" and "roux"
- by one tone (linguist jargon: *toneme*) - languages like Mandarin and
    Vietnamese have tones
- by the length of a sound (linguist jargon: *chroneme*) - e.g. Italian "vile"
    and "ville",
- when the stress is put on different syllables - e.g. English "address" (noun
    and verb), Greek "παπά" (priest) and "πάπα" (Pope).

For linguists, minimal pairs are most often used to "prove" that two
phonological units are different within a language.

But, for the average person, minimal pairs have a more practical use - language
learning! You can make tests with them: being given the audio pronunciation of a
word, you'll have to choose the word that you think was pronounced. Remember,
the more similar the sounds, the harder it is to get it correct! Also, note that
this "test" is made for both words, so you get to hear both pronunciations. With
time, after testing yourself consistently, you'll be able to better distinguish
the seemingly similar sounds of your target language.

Luckily, `grzegorz` can make Anki flashcards with exactly these kinds of tests,
helping you learn the sounds of your target language faster. Check the
[Usage](#usage) section!

## Getting started

### Requirements

For building:

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

If you want an to get an Anki deck full of minimal pairs without having to
bother too much with boring details, use `fullmake`:

```
$ grzegorz fullmake <language> <numwords> [--clean]
```

In other words, you tell it what language you want your minimal pairs in, and
the number of words to sample (the higher the sample, the more possible minimal
pairs found, although the runtime is longer), and, optionally, if it should
remove the files it made when running (`--clean` option).

So if you wanted to sample the 5000 most common Polish words, you'd do:

```
$ grzegorz fullmake Polish 5000
```

Check the "[Importing into Anki](#importing-into-anki)" section for information
on how you can use the deck in Anki-proper.

But if you want to manually go through the processes of creating a minimal pair
deck, then read ahead.

#### Manual

There are four commands, each corresponding to a single stage in the creation
process:

- `wordlist <language> <numwords> <output-file>`. The source for the wordlist is
    a frequency list based on movie subtitle occurences (check
    [hermitdave's FrequencyWords
    repository](https://github.com/hermitdave/FrequencyWords/tree/master/content/2016)).
    Please *don't* edit the wordlist file, as it will most likely result in errors.

- `fetchipa <wordlist> <output-file>`, which takes the output of `wordlist` and
    creates a JSON file where all words are paired with their International
    Phonetic Alphabet spelling, which is fetched from Wiktionary.

- `generate <ipa-json> <output-file> [--no-optimise | --no-phonemes |
    --keep-chronemes | --keep-stress]`, which takes the JSON file created by
    `fetchipa`, and outputs the list of minimal pairs it found, in JSON format.

    Note that, by default, it's optimised: it filters out pairs with "boring"
    differences which are easy to tell apart by most people ('q' and 't', 't'
    and 'd', 'e' and 'o' etc.). Give it the `--no-optimise` option to not curate
    the list.

    If you would like to keep minimal pairs based on chroneme and syllable
    stress differences, use the `--keep-chronemes` and `--keep-stress` options
    respectively. They're not enabled by default since they're computationally
    intensive.

    In a similar fashion, you can use the `--no-phomenes` option to discard
    minimal pairs based on phoneme differences.

- `makedeck <minpairs-list>`, which takes the output file of `generate` and
    creates an Anki deck package (`./grzegorz-anki-deck.apkg`) which you can
    import from inside Anki

##### Concrete example

Let's say you want to make a deck full of minimal pairs in French, without the
generator filtering out the "boring" pairs. Simple:

```
$ grzegorz wordlist french 5000 french-wordlist.txt
$ grzegorz fetchipa french-wordlist.txt french-ipas.json
$ grzegorz generate --no-optimise french-ipas.json french-minpairs.json
```

Then you could generate an Anki deck (output file: `grzegorz-anki-deck.apkg`, in
the current directory, no matter where the input file is located):

```
$ grzegorz makedeck french-minpairs.txt
```

### Importing into Anki

NOTE: the flashcards made don't have any audio, not because of a lack of
interest, but because of a lack of free (as in beer) APIs or libraries that can
(legally) furnish audio pronunciations. Forvo's API is paid! You must therefore
add it yourself, but it won't take a lot of time.

After you've created a deck package, open Anki, click on `Files` in the top left
corner, then `Import`, and then find the file and load it. A new deck,
"grzegorz's minimal pairs", should pop up. You can rename it, you can move it,
you can do anything with it. You also have control over its options, i.e. how
often you review it and whatnot.

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
