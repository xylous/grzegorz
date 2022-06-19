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

from .word import MinPair, readfile
import genanki
from genanki import Note, Deck
import json

# The model used for the flashcards is rather simple
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

def makedeck(infile: str) -> None:
    json_str = readfile(infile)
    dict = json.loads(json_str)
    minpairs = list(map(MinPair.from_dict, dict))
    notes = list(map(minpair_to_anki_note, minpairs))
    deck = notes_to_deck(notes)
    export_deck(deck)

### HELPER FUNCTIONS ###

# Given a minimal pair, create an Anki note from it, with grzegorz_minpair_model
# as its model.
def minpair_to_anki_note(minpair: MinPair) -> Note:
    first = minpair.first
    last = minpair.last
    note = genanki.Note(
        model=grzegorz_minpair_model,
        fields=[
            first.text,
            '',
            first.ipa,
            last.text,
            '',
            last.ipa,
        ]
    )
    return note

# Add a list of notes into a deck called "grzegorz's minimal pairs"
def notes_to_deck(notes: list[Note]) -> Deck:
    deck = genanki.Deck(
        1597757363,
        "grzegorz's minimal pairs",
    )
    for note in notes:
        deck.add_note(note)
    return deck

# Package the given deck and write it to a file
def export_deck(deck: Deck) -> None:
    outfile = 'grzegorz-anki-deck.apkg'
    genanki.Package(deck).write_to_file(outfile)
    print('Done! Now import', outfile, 'in your Anki')
