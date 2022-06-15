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

## Roadmap

- [x] fetch pronunciations for words
    - [x] in any language
    - [x] display a status bar
- [x] generate minimal pairs
    - [x] optimise: look for interesting differences
    - [x] optimise: ignore stressed syllables
- [ ] Anki integration

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GPLv3](./LICENSE)
