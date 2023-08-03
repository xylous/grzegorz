# The handy `fullmake` command

If you want to skip using the `wordlist`, `fetchipa`, `generate` and `makedeck`
commands manually, you can chain them automatically by using `fullmake`.

Its only parameters are the language name/code (remember that you may find
available languages by running `grzegorz list-languages`) and the number of
words to use as sample size.

For example, if you wanted to sample the first 10,000 words in the Polish
frequency list, you may run:

```
fullmake polish 10000
```

The result is an Anki deck, but the intermediary files which the other commands
create are also left over. If you want to delete said intermediary files and
keep only the Anki deck, you may use the `--clean` option:

```
fullmake polish 10000 --clean
```

Note that, personally, I do not advise using the `--clean` option, because
fetching the IPA transcriptions is a quite intensive process, and throwing it
all away in an instant seems wasteful. If you're completely sure you want to do
it, then go ahead.
