import MySQLdb
from datetime import datetime
import json

dbname = "automated_news_generator"
host = "localhost"
username = "root"
password = "1234"
summarizationconfig = "data/summarizationconfigforpilkada"

def connectDB(dbName):
    db = MySQLdb.connect(host, username, password, dbName)
    cursor = db.cursor()
    return db, cursor

def focusRetrieval(year, level, location, cycle):
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT entity_type FROM input_data, event WHERE input_data.event = event.event AND year=%s AND level='%s' AND event.location='%s' AND cycle='%s'" % (year, level, location, cycle)
    entity_type = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
        	entity_type.append(row[0])
    except:
        print('focus does not exist')
    db.close()
    return entity_type

def yearRetrieval():
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT year FROM event ORDER BY year"
    year = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            year.append(row[0])
    except:
        print('year does not exist')
    db.close()
    return year

def levelRetrieval(year):
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT level FROM event WHERE year=%s ORDER BY level" % (year)
    level = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            level.append(row[0])
    except:
        print('level does not exist')
    db.close()
    return level

def locationRetrieval(year, level):
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT location FROM event WHERE year=%s AND level='%s' ORDER BY level" % (year, level)
    locations = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            locations.append(row[0])
    except:
        print('location does not exist')
    db.close()
    return locations

def cycleRetrieval(year, level, location):
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT cycle FROM event WHERE year=%s AND level='%s' AND location='%s' ORDER BY cycle" % (year, level, location)
    cycles = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            cycles.append(row[0])
    except:
        print('cycle does not exist')
    db.close()
    return cycles

def valueTypeRetrieval(focus, year, level, location, cycle):
    db, cursor = connectDB(dbname)
    if focus == "Pasangan Calon":
        foc = "(input_data.entity_type = 'Pasangan Calon' OR input_data.entity_type = 'Pemilih')"
    else:
        foc = "input_data.entity_type = '" + focus + "'"
    query = "SELECT DISTINCT input_data.value_type FROM input_data, event, template WHERE input_data.value_type = template.value_type AND input_data.event = event.event AND %s AND year='%s' AND level='%s' AND cycle = '%s' AND event.location='%s'" % (foc, year, level, cycle, location)
    value_type = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            value_type.append(row[0])
    except:
        print('information does not exist')
    db.close()
    value_type.extend(derivedValueTypeRetrieval(focus))
    value_type = giveDefaultInfo(value_type)
    return value_type

def derivedValueTypeRetrieval(focus):
    value_type = []
    data = json.load(open(summarizationconfig))
    for rule in data:
        if rule["entity_type"] == focus or focus == "Pasangan Calon":
           value_type.append(rule["new_value_type"])
    return value_type

def giveDefaultInfo(types):
    value_type = []
    defaultType = ["Jumlah Suara", "Total Kemenangan", "Persentase Partisipasi Pemilih", "Jumlah Suara Sah", "Total DPT", "Persentase Partisipasi Pemilih", "Persentase Suara"]
    for vtype in types:
        if vtype in defaultType:
            value_type.append((vtype, "default"))
        else:
            value_type.append((vtype, "nondefault"))
    value_type = sorted(value_type, key=lambda tup: tup[1])
    return [ "%s,%s" % x for x in value_type]

def entityRetrieval(focus, year, level, location, cycle):
    entity = []
    if focus != "Pemilih":
        db, cursor = connectDB(dbname)
        query = "SELECT DISTINCT entity FROM input_data, event WHERE input_data.event = event.event AND entity_type='%s' AND year='%s' AND level='%s' AND cycle = '%s' AND event.location='%s'" % (focus, year, level, cycle, location)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                entity.append(row[0])
        except:
            print('entity does not exist')
        db.close()
    return entity

def subLocationRetrieval(focus, year, level, location, cycle):
    sublocation = []
    db, cursor = connectDB(dbname)
    query = "SELECT DISTINCT input_data.location FROM input_data, event WHERE input_data.event = event.event AND entity_type='%s' AND year='%s' AND level='%s' AND cycle = '%s' AND event.location='%s'" % (focus, year, level, cycle, location)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            sublocation.append(row[0])
    except:
        print('sublocation does not exist')
    db.close()
    return sublocation
    
def getTimeAndLocation():
    city = "Bandung"
    time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
    return city, time

def templateDBInsertion(template, value_type, rank, focus):
    db, cursor = connectDB(dbname)
    query = "INSERT INTO template (template, value_type, rank, entity_type, number_of_selection) VALUES ('%s', '%s', '%s', '%s', 0)" % (template, value_type, rank
        , focus)
    print(query)
    try:
       cursor.execute(query)
       db.commit()
       status = "ok"
    except:
       db.rollback()
       status = "error"
    db.close()
    return status
