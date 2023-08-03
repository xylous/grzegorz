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

Alternatively, using the language code:

```
grzegorz wordlist pl 20000 polish-wordlist.txt
```

You may also specify a lower and an upper bound instead of the absolute upper
bound, such as `25000:50000`, which takes only the words from index 25000 in the
word list up until index 50000. Here's an example of what that would look like:

```
grzegorz wordlist romanian 25000:50000 romanian-wordlilst.txt
```

But a wordlist on its own is rather underwhelming. There's one more step before
finding minimal pairs, and that is [fetching word IPAs](./ipa-fetch.md)
