# Copyright (c) 2022 xylous <xylous.e@gmail.com>
#
# This file is part of grzegorz.
# grzegorz is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# grzegorz is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# grzegorz.  If not, see <https://www.gnu.org/licenses/>.

from grzegorz.word import WordPair

import genanki
from genanki import Note, Deck

"""The model used for the flashcards is rather simple"""
grzegorz_minpair_model = genanki.Model(
    1958583115, # Randomly generated Model ID. Needs to be hardcoded!
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
            'qfmt':
"""<i>What did you hear?</i>

<br>

{{Word 1 audio}}

<br>

<div class="minpair">
<div id="correct-word" class="word">{{Word 1 text}}<br>{{Word 1 IPA}}</div>
<div class="center"><i>or</i></div>
<div class="word">{{Word 2 text}}<br>{{Word 2 IPA}}</div>
</div>""",
            'afmt':
"""{{FrontSide}}

<hr id=answer>

You heard: <div class="word">{{Word 1 text}}</div>

<script>
    var elem = document.getElementById("correct-word");
    elem.style.backgroundColor = '#26bf0b';
</script>""",
        },
        {
            'name': 'Card 2',
            'qfmt':
"""<i>What did you hear?</i>

<br>

{{Word 2 audio}}

<br>

<div class="minpair">
<div class="word">{{Word 1 text}}<br>{{Word 1 IPA}}</div>
<div class="center"><i>or</i></div>
<div id="correct-word" class="word">{{Word 2 text}}<br>{{Word 2 IPA}}</div>
</div>""",
            'afmt':
"""{{FrontSide}}

<hr id=answer>

You heard: <div class="word">{{Word 2 text}}</div>

<script>
    var elem = document.getElementById("correct-word");
    elem.style.backgroundColor = '#26bf0b';
</script>""",
        },
    ],
    css=
""".card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}

.word {
    text-align: center;
    border: 3px outset black;
    display: inline-block;
    box-sizing: border-box;
}

.nightMode .word {
    border: 3px outset white;
}

.minpair {
    display: flex;
    justify-content: center;
    align-items: center;
}

.center {
    display: inline;
    padding: 10px;
}""",
)

def minpairs_to_deck(minpairs: list[WordPair]) -> Deck:
    """Turn a list of minimal pairs into an Anki deck"""
    notes = [minpair_to_anki_note(mp) for mp in minpairs]
    return notes_to_deck(notes)

def export_deck(deck: Deck, outfile: str) -> None:
    """Package the given deck and write it to a file"""
    genanki.Package(deck).write_to_file(outfile)

def minpair_to_anki_note(minpair: WordPair) -> Note:
    """
    Given a minimal pair, create an Anki note from it, with `grzegorz_minpair_model`
    as its template.
    """
    note = genanki.Note(
        model=grzegorz_minpair_model,
        fields=[
            minpair[0].text,
            '',
            minpair[0].ipa,
            minpair[1].text,
            '',
            minpair[1].ipa,
        ]
    )
    return note

def notes_to_deck(notes: list[Note]) -> Deck:
    """
    Put the `Note`s into a `Deck` called "grzegorz's minimal pairs"
    """
    deck = genanki.Deck(
        1597757363, # deck ID, randomly generated but hardcoded
        "grzegorz's minimal pairs",
    )
    for note in notes:
        deck.add_note(note)
    return deck
