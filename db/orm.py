import uuid

from sqlalchemy import select, desc
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
            query = select(Templates.title, Templates.content).filter_by(id=id)
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

    @staticmethod
    def insert_new_message(message: dict):
        template_uuid = message['template']
        template = SyncOrm.select_template_by_id(template_uuid)
        templ_title = template[0]
        templ_content = template[1]

        with session_factory() as session:
            new_message = BroadcastMessages(
                id=uuid.uuid4(),
                title=templ_title,
                content=templ_content,
                show_to_trial=message['trial'],
                start_date=message['start_time'],
                finish_date=message['end_time'],
                creator_id=uuid.uuid4(),
                foreign=message['foreign'],
                include_emails=message['include_emails'],
                exclude_emails=message['exclude_emails']
            )
            session.add(new_message)
            session.commit()

    @staticmethod
    def select_last_message():
        with session_factory() as session:
            query = select(BroadcastMessages).order_by(desc(BroadcastMessages.created_date))
            res = session.execute(query).scalars().first()
            return res

