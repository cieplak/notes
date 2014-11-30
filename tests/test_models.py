from __future__ import unicode_literals

from notes.models import Note, Tag


def test_create_note():
    tags = ['todo', 'reminder']
    note = Note.create('note to self', tags=tags)
    tags_in_db = Tag.index()
    for tag in tags:
        assert tag in tags_in_db
        assert note in Tag.query.get(tag).notes
    assert note.tags == tags
