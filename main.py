#program entry
import helpers
import json
import os

SUFFIX = '.json'
DIR = 'tables'
OUTPUTFILE = 'newtestoutput'

def createParentheticalSchema(outputfilename):
    with open(OUTPUTFILE, 'w') as file:
        for filename in os.listdir(DIR):
            if filename.endswith(SUFFIX):
                query = getCreateTableQuery(filename)
                file.write(query)
        for filename in os.listdir(DIR):
            query = getForeignKeyConstraints(filename)
            if len(query) > 0:
                file.write(query)
    return

def getForeignKeyConstraints(filename):
    with open("{}/{}".format(DIR,filename)) as file:
        doc = json.load(file)
        filename = filename[:len(filename) - len(SUFFIX)]
        for field in doc['Fields']:
            if field['KeyType'] == "Foreign" or field["KeyType"] == 'Combined':
                return "ALTER TABLE {name} ADD CONSTRAINT FK_{keyname}{name} FOREIGN KEY ({keyname}) REFERENCES {ref}({keyname});\n".format(
                    name = filename, keyname = field["Name"], ref = field["Reference"])
            else:
                return ""

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
                if field['KeyType'] == "Primary" or field['KeyType'] == "Combined":
                    vals.append("CONSTRAINT PK_{0}{1} PRIMARY KEY ({0})".format(field["Name"], filename))
            query = "CREATE TABLE {name} ({vals});\n".format(name=filename, vals= ", ".join(vals))
            print(query)
            return query
        except:
            print("Failed to read {} fields".format(filename))
            return ""



createParentheticalSchema("something.sql")