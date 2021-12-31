import csv

def remap_columns(columns):
    names = {}
    for i in range(len(columns)):
        col = columns[i]
        if col in names:
            seq = names[col] + 1
            names[col] = seq 
            columns[i] = columns[i] + '_' + str(seq)
        else:
            names[col] = 0
    
    return columns

# handle csv file with duplicate field names when reading with csv.DictReader
def read_dict(file_name):
    rows = []
    with open(file_name, 'rt', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        columns = remap_columns(list(next(reader)))
        for row in reader:
            rows.append(dict(zip(columns, row)))
    
    return rows