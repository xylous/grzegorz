# Getting a decently-sized wordlist

The best candidate to finding a lot of minimal pairs is using a frequency list
for any given language.

`grzegorz` already provides functionality for getting one, through the
`wordlist` command. You tell it what language you want your wordlist in and the
number of words it should keep in it.

If you want to know what languages you can do that for, use the `list-languages`
function. You may use the language code or the language name itself.

Let's suppose you wanted to save the most common 20000 Polish words to a file
called `polish-wordlist.txt`. In your terminal, you would run:

```
grzegorz wordlist polish 20000 polish-wordlist.txt
```

Or, alternatively:

```
grzegorz wordlist pl 20000 polish-wordlist.txt
```

But a wordlist on its own is rather underwhelming. There's one more step before
finding minimal pairs, and that is [fetching word IPAs](./ipa-fetch.md)
