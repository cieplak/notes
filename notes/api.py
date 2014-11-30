from __future__ import unicode_literals
import json

from flask import Flask, request

from notes import models


app = Flask(__name__, static_url_path='')


def render(obj):
    return json.dumps(obj, default=lambda x: str(x))


@app.route('/')
def root():
    return '''{
"notes": "/notes",
"tags": "/tags",
"notes_by_tags": "/notes_by_tags",
"notes_under_tag": "/notes_under_tag"
}'''


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'GET':
        notes = [n.to_dict() for n in models.Note.index()]
        return render(notes), 200
    elif request.method == 'POST':
        payload = request.json
        id = payload.get('id')
        tags = payload.get('tags')
        note = payload.get('note')
        tags = tags.split()
        note = models.Note.create(note=note, tags=tags, id=id)
        models.Session.commit()
        return note.to_dict(), 201


@app.route('/tags', methods=['GET'])
def tags():
    return render(models.Tag.index())


@app.route('/tags/<tag>/notes', methods=['GET'])
def notes_under_tag(tag):
    serialized = [n.to_dict() for n in models.Note.index_by_tag(tag)]
    result = render(serialized)
    return result, 200


@app.route('/notes_by_tags', methods=['GET'])
def notes_by_tags():
    notes_by_tag = models.Note.index_by_tags()
    serialized = {
        tag: map(lambda note: note.to_dict(), notes_by_tag[tag])
        for tag in notes_by_tag
    }
    return render(serialized), 200


if __name__ == '__main__':
    app.run()
