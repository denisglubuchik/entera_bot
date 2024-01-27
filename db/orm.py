import uuid

from sqlalchemy import select, insert
from sqlalchemy.orm import sessionmaker

from .models import Templates, BotUsers, BroadcastMessages
from .db import engine


session_factory = sessionmaker(engine)


class SyncOrm:
    @staticmethod
    def select_templates():
        with session_factory() as session:
            query = select(Templates.id, Templates.title, Templates.content)
            res = session.execute(query)
            return res.all()

    @staticmethod
    def select_template_by_id(id):
        with session_factory() as session:
            query = select(Templates.title).filter_by(id=id)
            res = session.execute(query)
            return res.first()

    @staticmethod
    def insert_new_template(template: dict):
        templ_title = template['title']
        templ_content = template['content']
        with session_factory() as session:
            templ = Templates(
                id=uuid.uuid4(),
                title=templ_title,
                content=templ_content
            )
        session.add(templ)
        session.commit()

