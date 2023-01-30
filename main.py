"""Python script to import CSV files into Elasticsearch."""
import configparser
import csv
import glob
from elasticsearch import Elasticsearch

config = configparser.ConfigParser()
config.read("config.ini")
INDEX_NAME = "bible"

es = Elasticsearch(
    "http://" + config["ELASTIC"]["host"] + ":" + config["ELASTIC"]["port"]
)

files = glob.glob("./csv/*.csv")
for file in files:
    print(file)
    with open(file, "rt", encoding="utf8") as f:
        try:
            reader = csv.reader(f)
            for row in reader:
                bible_testament = row[0]
                bible_book = row[1]
                bible_chapter = row[2]
                bible_verse = row[3]
                bible_text = row[5]
                es.index(
                    index=INDEX_NAME,
                    document={
                        "testament": bible_testament,
                        "book": bible_book,
                        "chapter": bible_chapter,
                        "verse": bible_verse,
                        "text": bible_text,
                    },
                )
                print(f"{bible_testament} {bible_book} {bible_verse}")
        finally:
            f.close()
es.indices.refresh(index=INDEX_NAME)
