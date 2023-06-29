# "Interesting differences" between minimal pairs

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

### Custom filters

If you wanted to keep only minimal pairs that differ by `a`, `o` or `e`, or by
`f`, `t` and `d`, then your file would look something like:

```
a, o, e
f, t, d
```

And you would pass the name of your file to the generator via the
`--filter-file` option.
