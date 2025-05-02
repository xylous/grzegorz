# The minimal pair generator

Having [fetched IPA transliterations for your wordlist](./ipa-fetch.md), you may
now finally find minimal pairs.

This is done with the `generate` command; you give it the output of
`fetchipa` which contains IPA transliterations bound to words and it spews out
another file, this time with all the minimal pairs it found, in a [custom file
format](./formats.md).

By default, the `generate` command keeps minimal pairs based on phoneme
contrasts, chroneme contrasts and differences in syllable stress. You can
override this behaviour by using the following options:

- `--no-phonemes` - ignore phoneme-difference-based minimal pairs during generation
- `--no-chronemes` - ignore chroneme-difference-based minimal pairs during generation
- `--no-stress` - ignore minimal pairs based on syllable stress differences
    during generation

Also, by default, minimal pairs that contain phonemes that are ["interestingly
different"](./interesting-differences.md) are kept, and all others are ignored.
You may override this behaviour by using the `--no-optimise` option, which keeps
all minimal pairs found, or you may define your own "interesting differences"
[inside a file](./interesting-differences.md) and specify it with the
`--filter-file <PATH>` option, where `<PATH>` is the path to the file.

After finding minimal pairs, you may [create an Anki deck and import it into the
app](./anki-integration.md)

### Concrete examples

If your file containing the output of `fetchipa` is at `german-ipa.txt` and you
want to put the default output of `generate` in a file called
`german-minpairs.txt`, then you would run:

```
grzegorz generate german-ipa.txt german-minpairs.txt
```

If you wanted to keep *all* minimal pairs, except those based on syllable stress
differences, then you could run:

```
grzegorz generate ipa.txt minpairs.txt --no-stress --no-optimise
```

If you wanted to use your own filters for minimal pairs when optimising, and put
the file at `filters.txt`, then you would run:

```
grzegorz generate ipa.txt minpairs.txt --filter-file "filters.txt"
```
