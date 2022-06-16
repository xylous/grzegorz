# grzegorz

Grzegorz - a minimal pair generator.

> "That name is a hack to make the speaker bite themself"
- a wise discord user

~~Maybe deciding to start learning Polish wasn't a good choice.~~ I spent an
hour looking for a list of minimal pairs in Polish but in vain, I found nothing.
And so it struck me: I can just get a frequency list, slam it into a minimal
pair generator, and create my own list! But getting the pronunciations for such
a long list of words manually? No, I had to incorporate a pronunciation scraper
into this project. So practically, you give Grzegorz a list of words in plain
text, every word on its own line, and then the minimal pair generator is ran.

## Getting started

### Requirements

For building:

- python3
- pip

For running (install with `pip`):

- wiktionaryparser
- tqdm
- genanki

### Installation

##### Manual

Clone this repository, and run with python. Make sure you have all dependencies
installled.

```
git clone https://github.com/xylous/grzegorz grzegorz
cd grzegorz
python3 -m grzegorz --help
```

### Usage

There are two commands:

- `fetchpron`, which takes a file containing words separated by newlines, and,
    given the language you want your IPA pronunciations in, creates a JSON file
    at the specified output location

- `createpairs`, which takes the JSON file created before, and outputs the list
    of minimal pairs it found at the specified location.

    Note that, by default, it's optimised: it filters out pairs with "boring"
    differences which are easy to tell apart by most people ('q' and 't', 't'
    and 'd', 'e' and 'o' etc.). Give it the `--no-optimise` option to not curate
    the list.

    Secondly, syllable stress marks (`.`, `ˌ`, `ˈ`) are kept. You can use the
    `--ignore-stress` to discard them when generating minimal pairs.

- `ankideck`, which takes the output file of `createpairs` and creates an Anki
    deck package (`./grzegorz-anki-deck.apkg`) which you can import from inside
    Anki

So, how do you actually get the minimal pairs? You need to get the words from a
frequency list, that's obvious. I found [hermitdave's FrequencyWords
repository](https://github.com/hermitdave/FrequencyWords/tree/master/content/2016),
which contains word lists for a bunch of languages, but you could find other
lists elsewhere.

Note that `grzegorz` doesn't work with something like

```
1. the
tea hjkl
        bacon
...
```

Which it would not parse correctly. It won't even emit an error if the format is
wrong! Also, make sure there's no whitespace before or after the words.

The proper list would look like:

```
the
tea
bacon
...
```

So yes, you do have to make sure *all* words in the list are properly formatted.
You can usually find one on the internet fairly easily, and then you can use a
`sed` or an `awk` command to format, if it's not .

Let's assume your list is at `wordlist.txt`, and that it's full of French words:

```
grzegorz fetchpron "french" wordlist.txt processed.json
grzegorz createpairs processed.json minpairs.txt --ignore-stress
```

If you were to specify the wrong fetch language, shame on you: you'll likely end
up with the wrong pronunciations or none at all.

Then you could generate an Anki deck (output file: `grzegorz-anki-deck.apkg`, in
the current directory, no matter where the input file is located):

```
grzegorz ankideck minpairs.txt
```

After that, open Anki, click on `Files` in the top left corner, then `Import`,
and then find the package and load it. A new deck, "grzegorz's minimal pairs",
should pop up. You can rename it, you can move it, you can do anything with it.
You also have control over its options, i.e. how often you review it and whatnot.

## Roadmap

- [x] fetch pronunciations for words
    - [x] in any language
    - [x] display a status bar
- [x] generate minimal pairs
    - [x] optimise: look for interesting differences
    - [x] optimise: ignore stressed syllables
- [x] Anki integration
    - [x] create Anki flashcards from the generated minimal pairs
    - [x] export a deck containing the created flashcards
    - [ ] add pronunciations for every flashcard

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPLv3](./LICENSE)
