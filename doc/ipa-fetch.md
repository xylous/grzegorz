# Fetching all the necessary IPA transcriptions for words

After [getting a enough words](./wordlist.md), you'll need to get IPA
transcriptions for them.

Enter: the `fetchipa` command. You give it your wordlist and it spews back out
a [custom plain-text format](./formats.md) which is perfectly human readable.
Under the hood, it uses the [English Wiktionary](https://en.wiktionary.org), and
therefore the entire process is rather lengthy, both time-wise and
resource-wise. Also, there will be diminishing returns as the wordlist gets
bigger and bigger, because fewer and fewer transliterations will be found (if
you're using a frequency list, that is). So, the recommended wordlist size is
around 20.000 to 30.000 words, but you do you.

If you have a French wordlist at `french-words.txt`, and you'd wanted to store
the output in `french-words-with-ipa.txt`, you would simply run:

```
grzegorz fetchipa french-words.txt french-words-with-ipa.txt
```

The output file is updated constantly while the program is running. The main
advantage of this is that progress is never lost, and, in case of interruption,
you may pick up where it stopped by removing all the words in the wordlist up to
the last one found in the output file, and then re-running the same command.

By default, every word whose transliteration had not been found is not saved in
the output file. You can override this behaviour by using the `--keep-failed`
option, although in most cases you wouldn't need to.

You may also specify whether the number of threads that should handle processing
the wordlist by giving a number to the `--numproc` option. The default value is
twenty (20) threads. Theoretically, the more threads you have, the higher the
chance of Wiktionary enforcing rate limit, so don't try going overboard.

Now that you have IPA transliterations, it's time to have some real fun by
[finding the minimal pairs](./generator.md)
