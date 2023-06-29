# `grzegorz`'s user manual

`grzegorz` is a linguistics tool which primarily concerns minimal pairs.

## Commands

NOTE:
    - arguments whose placeholders are between `<` and `>` are mandatory, and
        those whose placeholders are between `[` and `]` are optional.
    - The extension added to placeholders indicate the filetype, e.g.
        `<WORDS_WITH_IPA.json>` is supposed to be a JSON file.

That being said, these are the commands and what they do:

- `analyse <IPA>` - print the result of phonologically parsing the provided IPA,
    in a human-readable format
- `check <IPA_1> <IPA_2>` - check if the two provided IPAs form a minimal pair;
    if they do, print the reason
- `list-languaegs` -  list all languages for which you can get a wordlist
- `wordlist <LANGUAGE> <NUMWORDS> <WORDLIST_FILE.txt>` - get a frequency list
    of `<NUMWORDS>` length and output it to `<WORDLIST_FILE.txt>`.
- `fetchipa <WORDLIST_FILE.txt> <WORDS_WITH_IPA.json> [--keep-failed]` - take
    the output of `wordlist` and create a JSON file where every word is
    associated with its IPA transcription, fetched from the English Wiktionary.
    - `--keep-failed` - keep entries for the words whose IPA was not found
        (default: don't)
    - NOTE: there are diminishing returns after a certain number of words
        because fewer and fewer of them have their IPA spelling on Wiktionary,
        so a sample size of around 20,000 or 30,000 words would be ideal.
    - NOTE: running this may take a while, especially with larger samples
- `generate <WORDS_WITH_IPA.json> <MINIMAL_PAIRS.json> [--no-optimise] [--no-phonemes]
    [--keep-chronemes] [--keep-stress] [-f | --filter-file <FILTER.txt>]` -
    takes the output of `fetchipa` and creates a JSON file with all the minimal
    pairs it found
    - `--no-optimise` - by default, only pairs with ["interesting
        differences"](#"interesting-differences") are kept, i.e. those that have
        sounds that are harder to differentiate, such as `/n/` and `/ŋ/`; use
        this option if you want to keep all possible minimal pairs, without
        filtering
    - `--no-phonemes` - do not keep minimal pairs that stem from phoneme
        differences (default: do)
    - `--keep-chronemes` - keep minimal pairs that are based on chroneme
        differences (default: don't)
    - `--keep-chronemes` - keep minimal pairs that are based on different
        syllable stress/articulation (default: don't)
    - `-f  | --filter-file <FILTER.txt>` - set custom minimal pair filters for
        ["interesting differences"](#"interestind-differences")
- `makedeck <MINIMAL_PAIRS.json> <ANKI_DECK.apkg>` - takes the output of
    `generate` and creates an Anki deck with flashcards containing them. NOTE:
    they don't have audio pronunciation.
- `fullmake <LANGUAGE> <NUMWORDS> [--clean]` - chain the `wordlist`, `fetchipa`,
    `generate` and `makedeck` commands. The `--clean` option specifies if only
    the Anki deck file should be created and all other files removed.

## "Interesting differences"

Some sounds are closer to each other, and so are harder to distinguish. By
default, `grzegorz` only keeps minimal pairs with slight differences. You can
use the `--no-optimise` option with the `generate` command to keep all possible
minimal pairs.

If you want to specify your own filters when generating minimal pairs, you'd
want to use the `grzegorz generate --filter-file <PATH>` option. The format used
is rather simple: every line contains comma-separated sounds which are
relatively close, and, therefore, form "interesting differences" in minimal
pairs. In other words, every minimal pair that differs by any two sounds on the
same line is kept. For example, these are the default "interesting differences"
that `grzegorz` looks after, in the proper file format:

```
t͡ɕ, t͡ʂ, t͡s, t͡ʃ, d͡ʐ, d͡ʑ, d͡z, d͡ʒ, ʂ, ʒ, ʃ, ɕ, zʲ, sʲ
n, ɲ, ŋ
v, f
x, h, xʲ, ç
z, ʑ, ʐ, s, ś, ʂ
ʎ, ɫ, l
ɟ, j, g, ɡʲ, g, ç
tʲ, tʰ, t ,d, dʲ, dʰ
r, ʁ

ɑ, a, ɐ, ə, ʌ, æ, ä, ɐ̯
ɑ, ə, œ
e, ɛ, ɪ, æ
ɨ, i, j, ɪ
ɔ, o, ø, œ, ɵ
ɥ, j
ɥ, u, ɤ, y, w, ɒ, ʊ, ʉ, ʊ̯
i, e

ɛ̃, ɛ
ɛ̃, ə
ɔ̃, ɔ
œ̃, œ, ɔ
ɛ̃, ɔ̃, œ̃, ɑ̃
```

If you wanted to keep only minimal pairs that differ by `a`, `o` or `e`, or by
`f`, `t` and `d`, then your file would look something like:

```
a, o, e
f, t, d
```

And you would pass the name of your file to the generator via the
`--filter-file` option.
