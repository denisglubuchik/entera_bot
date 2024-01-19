from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Db:
    db_url: str
    pg_admin: str
    pg_admin_password: str 


@dataclass
class Config:
    tgbot: TgBot
    db: Db


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN')),
                  db=Db(db_url=env('DB_URL'),
                        pg_admin=env('PGADMIN_USER'),
                        pg_admin_password=env('PGADMIN_PASSWORD')))