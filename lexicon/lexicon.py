LEXICON: dict[str, str] = {
    '/start': 'Это бот, в котором ты можешь узнать курс '
              'доллара на текущий момент\n\nЧтобы посмотреть список доступных '
              'команд - наберите /help',
    '/help': 'Это <b>бот-оповещатель.</b> Ты можешь узнать курс доллара '
             'на текущий момент\n\nДоступные команды:\n\n/dollar - '
             'узнать курс доллара (в рублях)\n/registry - зарегистрироваться '
             'для доступа к подписке на регулярное оповещение '
             'о курсе доллара\n/unregistry - удалить свой аккаунт '
             'и отменить подписку\n/history - получить историю запросов '
             'о курсе доллара',
    'dollar': 'Узнать курс 💲',
    'subscribe': 'Оформить подписку',
    'history': 'История запросов',
    'registry': 'Зарегистрироваться',
    'unregistry': 'Удалить аккаунт',
}

LEXICON_COMMANDS_RU: dict[str, str] = {
    '/help': 'Справка по работе бота',
    '/start': 'Запуск работы бота',
    '/dollar': 'Узнать курс доллара',
    '/registry': 'Регистрация аккаунта',
    '/unregistry': 'Удаление аккаунта',
    '/history': 'История запросов'
}
