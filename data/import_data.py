import csv

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from api.models import Category, Comment, CustomUser, Genre, Review, Title


def print_error(error, row, print_error):
    if print_error:
        print('Error:', error.args, '\nRow:', row)


def create_correct_row_fields(row, print_errors):
    try:
        if row.get('author'):
            row['author'] = CustomUser.objects.get(pk=row['author'])
        if row.get('review_id'):
            row['review'] = Review.objects.get(pk=row['review_id'])
        if row.get('title_id'):
            row['title'] = Title.objects.get(pk=row['title_id'])
        if row.get('category'):
            row['category'] = Category.objects.get(pk=row['category'])
        if row.get('genre'):
            row['genre'] = Genre.objects.get(pk=row['genre'])
    except ObjectDoesNotExist as error:
        print_error(error, row, print_errors)
    return row


def create_models(file_path, model, print_errors):
    with open(file_path, encoding='utf-8', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        total_count = 0
        successfull = 0
        for row in csv_reader:
            total_count += 1
            row = create_correct_row_fields(row, print_errors)
            try:
                model.objects.get_or_create(**row)
                successfull += 1
            except IntegrityError as error:
                print_error(error, row, print_errors)
            except ValueError as error:
                print_error(error, row, print_errors)
        errors = total_count - successfull
        print('Successfull: {}; errors: {}'.format(successfull, errors))


def import_data(print_errors=False):
    create_models('data/category.csv', Category, print_errors)
    create_models('data/titles.csv', Title, print_errors)
    create_models('data/genre.csv', Genre, print_errors)
    create_models('data/users.csv', CustomUser, print_errors)
    create_models('data/review.csv', Review, print_errors)
    create_models('data/comments.csv', Comment, print_errors)
