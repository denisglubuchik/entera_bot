BOT_LEXICON = {
    'start': 'Это Entera Bot для создания новых сообщений по шаблону',
    'help': 'Доступные команды: \n/new_message - создать новое сообщение'
            '\n/cancel - выйти из редактирования шаблона(введенные изменения'
            ' не сохраняются)',
    'cancel_default': 'Вы сейчас не редактируете никакой шаблон',
    'cancel_state': 'Вы вышли из редактирования шаблона',
    'new_message': 'Создать новое сообщение или выбрать шаблон',
    'choose_template': 'Выберите шаблон',
    'start_show': 'Введите время начала показа сообщения в формате\n'
                  '"2023-12-26 00:00"',
    'end_show': 'Введите время конца показа сообщения в формате\n'
                '"2023-12-26 00:00"',
    'russian/foreign': 'Показывать Российским или иностранным пользователям?',
    'trial': 'Показывать триальным пользователям?',
    'include_emails': 'Введите через запятую Emailы пользователей для которых'
                      ' показывать (если показывать всем пользователям '
                      'напишите "Всем")',
    'exclude_emails': 'Введите через запятую емейлы пользователей кому '
                      'НЕ показывать сообщение (если таких нет, напишите '
                      'НЕТ)',
    'not_date': 'Не валидная дата, по пробуйте еще раз',
    'not_email': 'Не валидный email, попробуйте еще раз',
    'successful_end': 'Сообщение сохранено\nЧтобы посмотреть данные вашего '
                      'сообщения - отправьте команду \n/show_message',
    'not_show_message': 'вы еще не отправляли сообщений, нажмите '
                        '/new_message, чтобы создать сообщение',
    'new_template_title': 'Напишите название нового шаблона',
    'new_template_content': 'Напишите содержание нового шаблона',
    'new_template_success': 'Новый шаблон сохранен',
    'new_template_cancel': 'Шаблон не был сохранен',
    'title': 'Введите название',
    'content': 'Введите содержимое сообщения',
    'edit_templates_button': '❌ РЕДАКТИРОВАТЬ',
    'del': '❌',
    'cancel_edit_templates': 'ОТМЕНИТЬ',
    'edit_templates_command': 'Вот ваши шаблоны, можете их редактировать',
    'finish_edit_templates': 'ЗАКОНЧИТЬ',
    'save': 'Выберите способ сохранения',
    'no_active_messages': 'Нет активных сообщений'
}

LEXICON_COMMANDS = {
    '/help': 'Справка по работе бота',
    '/templates': 'Список всех шаблонов',
    '/new_template': 'Создать новый шаблон',
    '/edit_templates': 'Редактировать, удалять шаблоны',
    '/new_message': 'Создать новое сообщение',
    '/show_message': 'Показать содержимое отправленного сообщения',
    '/cancel': 'Отменить отправку шаблона',
    '/show_active_messages': 'Показать активные сообщения'
}
