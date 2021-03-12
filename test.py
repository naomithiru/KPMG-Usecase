import json
# import mysql.connector
import sys


def save_to_db(json_file):
    json_data = open(json_file).read()
    # con = pymysql.connect(host='localhost', user='root', password="", db="")
    json_obj = json.loads(json_data)
    i = 0
    while i < 2:
        print(json_obj[i])
        i += 1


# save_to_db("src/scraping/output/responses_2018_now.json")
print(sys.path)
