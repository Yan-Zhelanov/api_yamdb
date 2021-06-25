# API YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

## Как импортировать дату в базу данных?
1. Используйте shell:
```bash
python manage.py shell
```

2. Импортируйте скрипт:
```python
from data.import_data import import_data
```
3. Запустите скрипт:
```python
# Если вам нужен отчёт о каждой ошибке:
import_data(True)

# Если не нужен:
import_data()
```

## Как импортировать дату из своего csv файла?
1. Заходим в shell:
```bash
python manage.py shell
```

2. Импортируем нужные модели:
```python
from api.models import User, Category, Comment, Genre, Review, Title
```

3. Импортируем скрипт:
```python
from data.import_data import create_models
```

4. Запускаем скрипт с тремя параметрами:

```file_path``` — путь до вашего csv файла,

```model``` — класс модели из импортированных ранее,

```print_errors``` — нужно ли распечатать каждую ошибку подробно? (```True or False```)

Пример:
```python
create_models('data/review.csv', Review, False)
```