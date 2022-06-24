# grzegorz

`grzegorz` - a minimal pair generator. For a detailed history of the project,
check the [Changelog](./Changelog.md)

If you already know about minimal pairs, or are just interested in linguistics,
you can use this project as learning material.

If use Anki to learn languages, you can use `grzegorz` to make an Anki deck full
of minimal pairs, helping you learn the sounds of your target language faster.
Check the [Usage](#usage) section!

But if you're not sure what minimal pairs are and what they're used for:

Consider that you're learning a new (real) language: like any beginner, you want
to learn the phonetics, both to be able to hear words and to be able to speak
(Tip: if you learn to it at the beginning of your journey, you won't have to
struggle fixing bad pronunciation habits later on). But, in order to learn the
sounds, you have to be able to differentiate between them. You won't get far if
you keep messing up your `ou`s and `u`s in French.

Enter: minimal pairs - pairs of words that differ by only *one* sound. Think:
bit - pit (english), rue - roux (french) etc. Or, more abstractly, when you test
yourself, a sound is played and then you have to choose between two very
similarly spelled words. After a few tests, your ability to *know* what sound
you heard increases, even outside of said tests.

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
pip install grzegorz
```

#### From source

Clone this repository and run pip:

```
git clone https://github.com/xylous/grzegorz grzegorz
cd grzegorz
pip install .
```

### Usage

If you want an to get an Anki deck full of minimal pairs without having to
bother too much with boring details, use `fullmake`:

```
grzegorz fullmake <language> <numwords> [--clean]
```

In other words, you tell it what language you want your minimal pairs in, and
the number of words to sample (the higher the sample, the more possible minimal
pairs found, although the runtime is longer), and, optionally, if it should
remove the files it made when running (`--clean` option).

So if you wanted to sample the 5000 most common Polish words (like me), you'd
do:

```
grzegorz fullmake "Polish" 5000
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
    `fetchipa`, and outputs the list of minimal pairs it found, in JSON format
    as well.

    Note that, by default, it's optimised: it filters out pairs with "boring"
    differences which are easy to tell apart by most people ('q' and 't', 't'
    and 'd', 'e' and 'o' etc.). Give it the `--no-optimise` option to not curate
    the list.

    If you would like to keep minimal pairs based on chroneme and syllable
    stress differences, use the `--keep-chronemes` and `--keep-stress` options
    respectively. They're not enabled by default since they're computationally
    intensive.

    In a similar fashion, you can use the `--no-phomenes` option to discard
    minimal pairs containing a difference in sounds.

- `makedeck <minpairs-list>`, which takes the output file of `generate` and
    creates an Anki deck package (`./grzegorz-anki-deck.apkg`) which you can
    import from inside Anki

##### Concrete example

Let's assume you want to make a deck full of minimal pairs in French.
and let's assume you didn't leave the installation directory (or else python
won't find the `grzegorz` module):

```
grzegorz wordlist "french" 5000 wordlist.txt
grzegorz fetchipa french-wordlist.txt french-ipas.json
grzegorz generate french-ipas.json minpairs.json --ignore-stress
```

If you were to specify the wrong wordlist language, shame on you: you'll likely
end up with the wrong International Phonetic Alphabet spellings or, worse, none
at all.

Then you could generate an Anki deck (output file: `grzegorz-anki-deck.apkg`, in
the current directory, no matter where the input file is located):

```
grzegorz makedeck minpairs.txt
```

## Importing into Anki

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
    - [x] optimise: look for interesting differences
    - [x] optimise: ignore stressed syllables
    - [x] look for phoneme contrasts
    - [x] look for chroneme differences
    - [x] look for syllable stress differences
- [ ] Anki integration
    - [x] create Anki flashcards from the generated minimal pairs
    - [x] export a deck containing the created flashcards
    - [ ] add audio pronunciations for every flashcard

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
