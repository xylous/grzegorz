# Quickshot phonological parsing

The characters used in IPA transcriptions not only represent sounds, but also
other important things, such as syllable stress (for example, you can see this
in the difference between "address" in English, noun and verb), or sound length,
or if a consonant forms a syllable on its own (yes, [those exist,
apparently](https://en.wikipedia.org/wiki/Syllabic_consonant)), or - you get the
idea.

`grzegorz` performs phonological parsing to better understand the transcriptions
it processes. Words are split into syllables, which may or may not be stressed,
and which themselves contain *phones* - no, not *tele*phones, [linguistic
phones!](https://en.wikipedia.org/wiki/Phone_(phonetics), which may be
themselves longer or shorter, as determined by the IPA transcription.

On your terminal, you can check the result of phonologically parsing any IPA.
Let's take the IPA transcription of the German word "spricht", which would be
"/ʃpʁɪ.çt/". So, for example, running `grzegorz analyse "/ʃpʁɪ.çt/"` will print:

```
/ʃpʁɪ.çt/
stress type: none
  [ "ʃ" "p" "ʁ" "ɪ" ]
stress type: none
  [ "ç" "t" ]
```

If a sound were to be long, then a `:` would be appended to it (note that [it is
not a colon, but a different character](https://en.wiktionary.org/wiki/%CB%90)).
Take, for example, the IPA for the French word "fête", "/fɛːt/". Running
`grzegorz analyse "/fɛːt/"` would return:

```
/fɛːt/
stress type: none
  [ "f" "ɛ:" "t" ]
```
