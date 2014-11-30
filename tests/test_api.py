from __future__ import unicode_literals
import json

from notes.api import app


def test_create_note():

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
