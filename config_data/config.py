from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


# @dataclass
# class Db:
#     db_url: str
#     pg_admin: str
#     pg_admin_password: str 


@dataclass
class Config:
    tgbot: TgBot


def load_config(path: str | None = None):
    env = Env()
    env.read_env(path)
    return Config(tgbot=TgBot(token=env('BOT_TOKEN')))