import datetime

from sqlalchemy import create_engine, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from config_data.config import config


# config: Config = load_config('.env')

db = config.db
engine = create_engine(
    f'postgresql+psycopg2://{db.pg_admin}:{db.pg_admin_password}'
    f'@{db.db_url}/{db.db_name}',
    echo=True
)

class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }
