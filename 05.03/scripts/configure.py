from pymongo import MongoClient
import csv
from constants import CONNECTION_URL, PATH, USERNAME, PASSWORD

def get_db():
    client = MongoClient(CONNECTION_URL % (USERNAME, PASSWORD))
    db = client['homework_05_03']
    return db

def load_dataset():
    db = get_db()
    with open(PATH, 'r') as dataset:
        reader = csv.DictReader(dataset)
        data = []
        for row in reader:
            data.append(row)
        print(len(data))
        db.mall.insert_many(data)

def main():
    load_dataset()

if __name__ == "__main__":
    main()