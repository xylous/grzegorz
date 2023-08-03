# Formats

`grzegorz` uses two custom plain-text data formats which are not only easily
encodable and decodable, but also human-readable.

The first data format is for single words: the word's letters, followed by a
comma and a space (`, `), followed by the IPA transliteration. At most one entry
per line in a file. If there is no transliteration, then the structural
representation of said word has none. Thus, the English word "bard" and its IPA
transcription, "/bɑːd/", would be encoded as: `bard, /bɑːd/`.

The second data format is for minimal pairs, with a single minimal pair per
line. It separates two encoded words with a space, two dashes, and another
space, i.e. ` -- `. Thus, an encoded minimal pair would look like: `bard, /bɑːd/
-- fard, /fɑːd/`.
