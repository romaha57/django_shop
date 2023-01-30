## Онлайн магазин созданный на фраймворке Django

Функционал сайта:
- позволяет просматривать каталог товаров
- позволяет фильтровать по категориям
- есть возможность добавлять товары в корзину и удалять их
- также есть система авторизации и аутентификации на сайте
- проработан личный кабинет пользователя с возможностью редактирования данных
- сделана страница с просмотром истории заказов и переход на конкретный заказ
- сделана система оплаты товаров(тестовая, через stripe)
- добавлена функция подтверждения почты(письмо отправляется на почту с ссылкой для подтверждения mail)

Основные библиотеки, использованные в проекте: 
*Django, DRF, Redis(кеш и работа с очередью задач), Celery*

СУБД, используемая в проекте: 
*Postgres*