#program entry
import helpers
import json
import os

SUFFIX = '.json'
DIR = 'tables'

def createParentheticalSchema(outputfilename):
    for filename in os.listdir(DIR):
        if filename.endswith(SUFFIX):
            getCreateTableQuery(filename)
    return

def getCreateTableQuery(filename):
    with open("{}/{}".format(DIR,filename)) as file:
        doc = json.load(file)
        filename = filename[:len(filename) - len(SUFFIX)]
        # attempt to read fields
        try:
            vals = []
            for field in doc['Fields']:
                nullable = "NOT NULL"
                if field["Nullable"] == "True":
                    nullable = ""
                vals.append("{} {} {}".format(field["Name"], field["Type"], nullable))
                if field['KeyType'] == "Primary":
                    vals.append("CONSTRAINT PK_{0} PRIMARY KEY ({0})".format(field["Name"]))
            query = "CREATE TABLE {name} ({vals});".format(name=filename, vals= ", ".join(vals))
            print(query)
            return query
        except:
            print("Failed to read {} fields".format(filename))
            return ""



createParentheticalSchema("something.sql")