# API YaMDb
The YaMDb project collects user reviews of works of art.
Works have different categories: "Books", "Movies", "Music".

## How to import data
1. Use shell to import:
```bash
python manage.py shell
```

2. Import script:
```python
from data.import_data import import_data
```
3. Run script:
```python
# If you need print errors:
import_data(True)

# or:
import_data()
```

## How to import custom data
1. Use shell to import:
```bash
python manage.py shell
```

2. Import all models what you need:
```python
from api.models import CustomUser, Category, Comment, Genre, Review, Title
```

3. Import script:
```python
from data.import_data import create_models
```

4. Run script with three parameters:
```file_path```,
```model``` — Class model,
```print_errors``` — do need to print errors
Example:
```python
create_models('data/category.csv', Category, False)
```