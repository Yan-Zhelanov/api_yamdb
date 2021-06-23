import csv


def create_models(file_path, model):
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        column_count = 0
        fields = []
        data = {}
        for row in csv_reader:
            for column in row:
                if line_count == 0:
                    fields.append(column)
                else:
                    data[fields[column_count]] = column
                    column_count += 1
                    if column_count > (len(fields) - 1):
                        model.objects.create(data)
                        column_count = 0

# from api.models import User
# from data.import_data import create_models
# create_models('data/users.csv', User)