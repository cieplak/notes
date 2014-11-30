from __future__ import unicode_literals
import json

from notes.api import app
from notes.models import Session, db_init


def test_create_note():
    db_init()
    client = app.test_client()
    body = dict(
        id='b060',
        note='note to self',
        tags='reminder todo',
    )
    client.post('/notes', data=json.dumps(body))
    notes = json.loads(client.get('/notes').data)
    expected_notes = [
        dict(
            id='b060',
            note='note to self',
            tags=['reminder', 'todo'],
            state='PENDING',
        )
    ]
    for note in notes:
        note.pop('timestamp')
    assert notes == expected_notes
    tags = json.loads(client.get('/tags').data)
    expected_tags = ['reminder', 'todo']
    assert tags == expected_tags


def test_notes_by_tags():
    db_init()
    client = app.test_client()
    note1 = dict(
        note='buy oil; change oil',
        tags='car grocery',
    )
    note2 = dict(
        note='butter',
        tags='grocery',
    )
    note3 = dict(
        note='michael from cocktail party',
        tags='name',
    )
    notes = [note1, note2, note3]
    for note in notes:
        client.post('/notes', data=json.dumps(note))
    expected_view = {
        'car': [
            {'note': 'buy oil; change oil', 'tags': ['car', 'grocery']}
        ],
        'grocery': [
            {'note': 'buy oil; change oil', 'tags': ['car', 'grocery']},
            {'note': 'butter', 'tags': ['grocery']}
        ],
        'name': [
            {'note': 'michael from cocktail party', 'tags': ['name']}
        ],
    }
    view = json.loads(client.get('/notes_by_tags').data)
    note_attributes_to_pop = ['id', 'timestamp', 'state']
    for tag in view:
        notes = view[tag]
        for note in notes:
            for attr in note_attributes_to_pop:
                note.pop(attr)
    assert view == expected_view

def test_note_under_tag():
    db_init()
    client = app.test_client()
    note = dict(
        note='buy oil; change oil',
        tags='car grocery',
    )
    client.post('/notes', data=json.dumps(note))
    resp = client.get('/tags/car/notes')
    view = json.loads(resp.data)
    expected_view = [
        {'note': 'buy oil; change oil', 'tags': ['car', 'grocery']},
    ]
    for attr in ['id', 'timestamp', 'state']:
        view[0].pop(attr)
    assert view == expected_view
