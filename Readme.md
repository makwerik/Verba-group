# Парсер сайта https://quotes.toscrape.com/

### Описание
Парсер создан для выполнения тестового задания для компании VERBA-group.

Реализовано два класса парсера:
1. [Обычный парсер (scrapper.py)](https://github.com/makwerik/Verba-group/blob/master/scrapper.py)
2. [Асинхронный парсер (scrapper_async.py)](https://github.com/makwerik/Verba-group/blob/master/scrapper_async.py)
3. [main (main.py)](https://github.com/makwerik/Verba-group/blob/master/main.py) - оставил, так как это был черновой вариант, чтобы понять что и как откуда получить
4. [page (page.py)](https://github.com/makwerik/Verba-group/blob/master/page.py)- тоже оставил, тут я реализовывал получение страниц

### Обычный парсер (scrapper.py)
Для реализации обычного парсера использовались следующие библиотеки:
- `requests` — для отправки HTTP-запросов.
- `bs4` (BeautifulSoup) — для парсинга HTML-страницы.
- `fake-useragent` — для эмуляции разных user-agent, чтобы избежать блокировок со стороны сервера.
- `json` — для сохранения данных в файл.

Парсер реализован в виде класса `Scrapper`, который включает базовый инициализатор с возможностью указания URL (по умолчанию используется https://quotes.toscrape.com). Класс построен так, что каждый метод выполняет свою отдельную задачу, с несколькими приватными методами и одним публичным методом для управления процессом парсинга. Сбор данных осуществляется через `div` и `class` разметку на HTML-странице, так как `fetch/xhr` не показывает запросы для получения готовых JSON-данных.

Задержка между запросами не реализована, так как сайт состоит всего из 10 страниц, и вероятность блокировки мала.

### Асинхронный парсер (scrapper_async.py)
Асинхронный парсер имеет тот же функционал, но реализован с использованием следующих библиотек:
- `aiohttp` — для асинхронных HTTP-запросов.
- `asyncio` — для управления асинхронными задачами.

Запросы выполняются на основе сессий, и в отличие от обычного парсера, в асинхронной версии используется асинхронное программирование для повышения производительности. Поскольку мой опыт в асинхронном программировании ограничен, приходилось обращаться к документации и дополнительным источникам для понимания использования `aiohttp` и `asyncio`.
