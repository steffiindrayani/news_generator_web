# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:59:51 2018

@author: Steffi Indrayani
"""

import MySQLdb
import json

dbname = "automated_news_generator"

"""
Connect to DB
Input   : Name of Database (String)
Output  : Connection to Database, Cursor
"""
def connectDB(dbName):
    host = "localhost"
    username = "root"
    password = "1234"
    db = MySQLdb.connect(host, username, password, dbName)
    cursor = db.cursor()
    return db, cursor
    
"""
Retrieve data based on query
Input   : Database Query (String)
Output  : List of Data (List of dictionary)
          Data consists of:
          entity_type (str), entity (str), location_type (str), location (str),
          value_type (str), value (number), event_type (str), event (str)
"""    
def dataRetrieval(query):
    db, cursor = connectDB(dbname)
    contents = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        #Fetch Data
        for row in results:
            data = dict()
            data['entity_type'] = row[0]
            data['entity'] = row[1]
            data['location_type'] = row[2]
            data['location'] = row[3]
            data['value_type'] = row[4]
            data['value'] = row[5]
            data['event_type'] = row[6]
            data['event'] = row[7]
            contents.append(data)
    except:
        print("Error: unable to fetch data")
    db.close()
    return contents

"""
Create query based on request
Input   : POST Request (dict)
          A POST request consists of:
          entity (list of str), year (list of int), focus of news(list of str), level (list of str), cycle (list of int), 
          location of event (list of str), sublocation/location of selection (list of str), value_type (list of str)
Output  : Database Query (str), Request (dict)
          A request consists of
          location request (str), event (str), focus of news (str), location of event (str), entity (str), 
          sublocation (str), value_type (list of str)
"""     
def readQuery(request):
    print("Pembangkit Berita Pemilihan Kepala Daerah di Indonesia")
    calon = request["entity"][0]
    tahun = request["year"][0]
    fokus = request["focus"][0]
    tingkat = request["level"][0]
    daerah = request["location"][0]
    putaran = request["cycle"][0]
    #Define cycle in text form
    if (putaran == 1):
        putaran = "Pertama"
    else:
        putaran = "Kedua"
    lokasi = request["sublocation"][0]
    value_type = request["value_type"]
    #define event
    event = "Pemilihan " + tingkat + " " + daerah + " " + tahun + " Putaran " + putaran
    request = dict()
    loc = ""
    if lokasi != "":
        loc = lokasi
    else:
        loc = daerah

    #Summarize request
    request["loc"] = loc
    request["event"] = event
    request["fokus"] = fokus
    request["daerah"] = daerah
    request["calon"] = calon
    request["lokasi"] = lokasi
    request["value_type"] = value_type

    #Define query
    query = "SELECT * FROM input_data WHERE event = '%s'" % (event)
    if fokus != "":
        if fokus == "Pasangan Calon":
            query += " AND (entity_type='pemilih' OR entity_type='%s')" % (fokus)
        else:
            query += " AND entity_type='%s'" % (fokus)
        
    if calon != "":
        query += " AND (entity='%s' OR entity_type ='pemilih')" % (calon)        

    query += " AND (location='%s'" % (loc)
    query += " OR location IN (SELECT location FROM location WHERE super_location='%s'))" % (loc)
    
    query += " AND ("
    for i in range(0, len(value_type)):
        if i != 0:
            query += " OR"
        query += " value_type = '%s'" % (value_type[i]) 
    query += ")"
    query += " ORDER BY location, value desc"
    return query, request

"""
Read JSON File and return data inside the file
Input   : File Name (str)
Output  : Data (dict or list)
"""     
def readJsonFile(filename):
    data = json.load(open(filename))
    return data

"""
Retrieva Template from Database
Input   : Database Query (str)
Output  : Template (dict)
          A template consists of:
          id (int), template sentence (str), entity_type condition (str), value_type condition (str),
          id template couple (int), location condition (str), rank condition (str)
"""     
def templateRetrieval(query):
    db, cursor = connectDB(dbname)
    template = dict()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        #Fetch Data        
        for row in results:
            template["id"] = row[0]
            template["template"] = row[1]
            template["entity_type"] = row[2]
            template["value_type"] = row[3]
            if row[4] is None:
                template["couple"] = 0
            else:
                template["couple"] = row[4]
            template["location"] = row[5]
            template["rank"] = row[6]
        templateUpdateNumberofSelection(template["id"])
    except:
        print("")
    db.close()
    return template

"""
Update Number of Template Selection
Input   : id Template (int)
F.S.    : Number of selection from the selected template will be added by 1
"""        
def templateUpdateNumberofSelection(idtemp):
    db, cursor = connectDB(dbname)
    query = "UPDATE template SET number_of_selection = number_of_selection + 1 WHERE id = '%d'" % (idtemp)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()    

"""
Retrive aggregated template
Input   : Database Query (str)
Output  : value_type from first template (str), template sentence (str)
"""      
def aggregationTemplateRetrieval(query):
    db, cursor = connectDB(dbname)
    template = ""
    value_type1 = ""
    try:
        cursor.execute(query)
        results = cursor.fetchall()   
        #Fetch Data        
        for row in results:
            value_type1 = row[0]
            template = row[1]
    except:
        print("Error: unable to fetch data")
    db.close()
    return value_type1, template

"""
Retrieve Entity Fact
Input   : Database Query (str)
Output  : Entity fact (str)
          Return only value if value_type = Alias, e.g. "Ahok Djarot"
          else return entity_type + " dengan " + value_type + " " + value, e.g. "Pasangan Calon dengan Nomor Urut 2" 
""" 
def entityFactRetrieval(query):
    db, cursor = connectDB(dbname)
    entity_type = ""
    value_type = ""
    value = ""
    try:
        #Fetch Data
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            idfact = row[0]
            entity_type = row[1]
            value_type = row[2]
            value = row[3]
        factUpdateNumberofSelection(idfact)
    except:
        return ""
    db.close()
    if value_type == "Alias":
        return value
    return entity_type + " dengan " + value_type + " " + value   


"""
Update Number of Fact Selection
Input   : id Fact (int)
F.S.    : Number of selection from the selected entity fact will be added by 1
"""       
def factUpdateNumberofSelection(idfact):
    db, cursor = connectDB(dbname)
    query = "UPDATE entity_fact SET number_of_selection = number_of_selection + 1 WHERE id = '%d'" % (idfact)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()    

