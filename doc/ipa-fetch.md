# Fetching all the necessary IPA transcriptions for words

After [getting a enough words](./wordlist.md), you'll need to get IPA
transcriptions for them.

Enter: the `fetchipa` command. You give it your wordlist and it spews back out
some JSON which binds every transliteration to the word. Under the hood, it uses
the [English Wiktionary](https://en.wiktionary.org), and therefore the entire
process is rather lengthy, both time-wise and resource-wise. Also, there will be
diminishing returns as the wordlist gets bigger and bigger, because fewer and
fewer transliterations will be found (if you're using a frequency list, that
is). So, the recommended wordlist size is around 20.000 to 30.000 words, but you
you do you.

If you have a French wordlist at `french-words.txt`, and you'd wanted to store
the output in `french-words-with-ipa.json`, you would simply run:

```
grzegorz fetchipa french-words.txt french-words-with-ipa.json
```

By default, every word whose transliteration had not been found is not saved in
the JSON file. You can override this behaviour by using the `--keep-failed`
option, although in most cases you wouldn't need to.

Now that you have IPA transliterations, it's time to have some real fun by
[finding the minimal pairs](./generator.md)
