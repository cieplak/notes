from __future__ import unicode_literals
from datetime import datetime
import json
import uuid

from sqlalchemy import (
    Column, DateTime, ForeignKey, Table, Unicode, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

from notes import settings

engine = create_engine(settings.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = Session.query_property()


def db_init():
    Base.metadata.create_all(engine)


note_tag_associations = Table(
    'note_tag_associations', Base.metadata,
    Column('tag', Unicode, ForeignKey('tags.tag')),
    Column('note_id', Unicode, ForeignKey('notes.id')),
)


class Note(Base):

    __tablename__ = 'notes'

    id = Column('id', Unicode, primary_key=True,
                default=lambda: uuid.uuid4().hex)
    timestamp = Column('timestamp', DateTime, default=datetime.utcnow)
    note = Column('note', Unicode)
    state = Column('state', Unicode)
    _tags = relationship('Tag', secondary=note_tag_associations, backref='notes')

    @property
    def tags(self):
        return [t.tag for t in self._tags]

    @classmethod
    def index(cls):
        return Note.query.all()

    @classmethod
    def create(cls, note, id=None, state='PENDING', tags=[]):
        kwargs = dict(note=note, state=state)
        if id:
            kwargs['id'] = id
        note = Note(**kwargs)
        Session.add(note)
        Session.flush()
        for tag in tags:
            note.tag(tag)
        return note

    def tag(self, tag):
        Tag.create(tag)
        Session.execute(note_tag_associations.insert(
            values=dict(tag=tag, note_id=self.id)
        ))
        return tag

    def to_dict(self):
        return dict(
            id=self.id,
            timestamp=self.timestamp,
            note=self.note,
            state=self.state,
            tags=self.tags,
        )

    def to_json(self):
        return json.dumps(self.to_dict(), default=lambda x: str(x))


class Tag(Base):

    __tablename__ = 'tags'

    tag = Column('tag', Unicode, primary_key=True)

    @classmethod
    def create(cls, tag):
        if tag in cls.index():
            return tag
        tag = Tag(tag=tag)
        Session.add(tag)
        Session.flush()
        return tag.tag

    @classmethod
    def index(cls):
        return [t.tag for t in Tag.query]
