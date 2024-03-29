from aiogram.fsm.state import State, StatesGroup


class FillTemplate(StatesGroup):
    new_or_template = State()
    fill_title = State()
    fill_content = State()
    choose_template = State()
    fill_start_time = State()
    fill_end_time = State()
    fill_where_users_from = State()
    fill_trial_users = State()
    fill_include_emails = State()
    fill_exclude_emails = State()
    fill_save_or_not = State()


class Template(StatesGroup):
    fill_title = State()
    fill_content = State()
    accept_template = State()
    edit_templates = State()