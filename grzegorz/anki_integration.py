from .word import Word, readfile
import genanki

grzegorz_minpair_model = genanki.Model(
    # Randomly generated Model ID.
    1958583115,
    'Grzegorz Minimal Pairs',
    fields=[
        {'name': 'Word 1 text'},
        {'name': 'Word 1 audio'},
        {'name': 'Word 1 IPA'},
        {'name': 'Word 2 text'},
        {'name': 'Word 2 audio'},
        {'name': 'Word 2 IPA'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': 'What do you hear?<br>{{Word 1 audio}}<br>{{Word 1 text}} OR {{Word 2 text}}',
            'afmt': '{{FrontSide}}<hr id=answer>{{Word 1 text}}<br>{{Word 1 IPA}}',
        },
        {
            'name': 'Card 2',
            'qfmt': 'What do you hear?<br>{{Word 2 audio}}<br>{{Word 1 text}} OR {{Word 2 text}}',
            'afmt': '{{FrontSide}}<hr id=answer>{{Word 2 text}}<br>{{Word 2 IPA}}',
        },
    ],
    css="""
.card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}
    """,
)

def line_to_minpair(line):
    line = line.split()
    word1 = Word(line[0], line[1])
    word2 = Word(line[-2], line[-1])
    return (word1, word2)

def parse_input_file(path):
    lines = readfile(path).splitlines()
    minpairs = list(map(line_to_minpair, lines))
    return minpairs

def minpair_to_anki_note(minpair):
    word1, word2 = minpair
    note = genanki.Note(
        model=grzegorz_minpair_model,
        fields=[
            word1.text,
            '',
            word1.ipa,
            word2.text,
            '',
            word2.ipa,
        ]
    )
    return note
