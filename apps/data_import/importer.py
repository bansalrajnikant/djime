from csv import DictReader

def handle_uploaded_file(file):
    dict = csv.DictReader(file)
    value_list = []
    for value in dict:
        value_list.append(value)
     
