from __future__ import unicode_literals
import json

from flask import Flask, request

from notes import models


app = Flask(__name__, static_url_path='')


def render(obj):
    return json.dumps(obj, default=lambda x: str(x))


@app.route('/')
def root():
    return '{"notes": "/notes", "tags": "/tags"}'


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'GET':
        notes = [n.to_dict() for n in models.Note.index()]
        return render(notes)
    elif request.method == 'POST':
        payload = json.loads(request.data)
        id = payload.get('id')
        tags = payload.get('tags')
        note = payload.get('note')
        tags = tags.split()
        note = models.Note.create(note=note, tags=tags, id=id)
        return str(note.id), 201


@app.route('/tags', methods=['GET'])
def tags():
    return render(models.Tag.index())


@app.route('/tags/<tag>/notes', methods=['GET'])
def notes_under_tag(tag):
    pass


if __name__ == '__main__':
    app.run()
