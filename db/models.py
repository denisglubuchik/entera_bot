import datetime
import uuid
import sqlalchemy as sa
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB

from .db import Base, engine
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

session_factory = sessionmaker(engine)
uuidpk = Annotated[uuid.UUID, mapped_column(sa.types.Uuid, primary_key=True)]


class BotUsers(Base):
    __tablename__ = 'bot_users'

    id: Mapped[uuidpk]
    username: Mapped[str]
    tg_id: Mapped[int]


class Templates(Base):
    __tablename__ = 'templates'

    id: Mapped[uuidpk]
    title: Mapped[str]
    content: Mapped[str]


class BroadcastMessages(Base):
    __tablename__ = 'broadcast_message'

    id: Mapped[uuidpk]
    title: Mapped[str]
    content: Mapped[str]
    show_to_trial: Mapped[bool] = mapped_column(default=False)
    start_date: Mapped[datetime.datetime]
    finish_date: Mapped[datetime.datetime]
    include_emails: Mapped[list | None] = mapped_column(JSONB)
    exclude_emails: Mapped[list | None] = mapped_column(JSONB)
    created_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now(),
                                                            onupdate=datetime.datetime.now())
    modified_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    version: Mapped[int] = mapped_column(default=1)
    creator_id: Mapped[uuid.UUID] = mapped_column(sa.types.Uuid)
    message_type: Mapped[str] = mapped_column(default='POLL')
    foreign: Mapped[bool] = mapped_column(default=False)


# def insert_data():
#     with session_factory() as session:
#         message = BroadcastMessages(
#             id=uuid.uuid4(),
#             title='qweqwe',
#             content='asdasdasd',
#             show_to_trial=False,
#             start_date='2023-12-26 00:00',
#             finish_date='2023-12-26 00:00',
#             creator_id=uuid.uuid4(),
#             foreign=True
#         )
#         session.add_all([message])
#         session.commit()


