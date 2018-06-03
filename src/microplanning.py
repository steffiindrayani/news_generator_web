# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:04:27 2018

@author: Steffi Indrayani
"""

from src.input_handler import templateRetrieval, aggregationTemplateRetrieval

def microplanning(documentPlan, request):
    print("lexicalising...")
    lexicalisation(documentPlan, request)
    print("aggregating...")
    documentPlan = aggregation(documentPlan)
    print("assigning REG..")
    assignREG(documentPlan)
    return documentPlan
    
# def lexicalisation(documentPlan, request):
#     for contents in documentPlan:
#         couple = 0
#         for data in contents:
#             id_template, template, couple = getTemplate(data, request["lokasi"], couple)
#             data["id_template"] = id_template
#             data["template"] = template

def lexicalisation(documentPlan, request):
    for contents in documentPlan:
        couple = 0
        existingTemplates = []
        for data in contents:
            id_template, template, couple = searchExistingTemplate(data, existingTemplates, couple)
            if id_template != 0:
                data["id_template"] = id_template
                data["template"] = template
            else:
                template,couple = getTemplate(data, request["lokasi"], couple)
                data["id_template"] = template["id"]
                data["template"] = template["template"]
                template["prevlocation"] = data["location"]
                #template["preventity"] = data["entity"]
                existingTemplates.append(template)
                
                
def assignREG(documentPlan):
    entity = []
    for contents in documentPlan:
        for i in range (0, len(contents) - 1):
            if (contents[i]["entity"] == contents[i+1]["entity"]):
                contents[i+1]["REG"] = "True"
            else:
                if contents[i+1]["entity"] in entity:
                    contents[i+1]["REG"] = "Alias"
                else:
                    entity.append(contents[i+1]["entity"])
            if i == 0:
                if contents[i]["entity"] in entity:
                    contents[i]["REG"] = "Alias"
                else:
                    entity.append(contents[i]["entity"])

# def aggregation(documentPlan):
#     for contents in documentPlan:
#         for i in range (0, len(contents) - 1):
#             if contents[i]["id_template"] != 0:
#                 idtemp, template = getAggregationTemplate(contents[i],contents[i+1])
#                 if template != "":
#                     contents[i]["id_template"] = idtemp
#                     contents[i]["template"] = template
#                     contents[i+1]["id_template"] = 0
#                     contents[i+1]["template"] = ""

def aggregation(documentPlan):
    deprecatedContents = []
    for i in range(0, len(documentPlan)):
        aggregateUsingTemplate(documentPlan[i])
        aggregateSimilarSentences(documentPlan[i])
        if not isValidContents(documentPlan[i]):
            deprecatedContents.append(i)
    if len(deprecatedContents) > 0:
        documentPlan = mergeGroups(documentPlan, deprecatedContents)
        deprecatedContents = []
        for i in range(0, len(documentPlan)):
            if not isValidContents(documentPlan[i]):
                print("here")
                deprecatedContents.append(i)
        if len(deprecatedContents) > 0:
            documentPlan = mergeGroups1(documentPlan, deprecatedContents)
    return documentPlan
        
def aggregateUsingTemplate(contents):
    for i in range (0, len(contents) - 1):
        if contents[i]["id_template"] != 0:
            idtemp, template = getAggregationTemplate(contents[i],contents[i+1])
            if template != "":
                contents[i]["id_template"] = idtemp
                contents[i]["template"] = template
                contents[i+1]["id_template"] = 0
                contents[i+1]["template"] = ""

def aggregateSimilarSentences(contents):
    idx = len(contents) - 1
    while True:
        if contents[idx]["id_template"] != 0:
            break
        else:
            idx -= 1
    aggregated = False
    for i in range (idx - 1, -1, -1):
        if contents[i]["id_template"] != 0:
            if contents[i]["id_template"] == contents[idx]["id_template"]:
                #remove tanda titik dan perkecil kata kedua, konjungsi random, cek pernah gak
                contents[i]["template"] = contents[i]["template"].rstrip('.')
                contents[i]["aggregated"] = 'True' 
                if aggregated:
                    contents[idx]["template"] = ", " + contents[idx]["template"][:1].lower() + contents[idx]["template"][1:] 
                else:
                    contents[idx]["template"] = ", sedangkan " + contents[idx]["template"][:1].lower() + contents[idx]["template"][1:] 
                if (contents[i]["location"] == contents[idx]["location"]):
                    contents[idx]["template"] = contents[idx]["template"].replace(" di {{location}},", "")
                    contents[idx]["template"] = contents[idx]["template"].replace(" di {{location}}", "")
                aggregated = True
            else:
                aggregated = False
            idx = i
                
# def getTemplate(data, lokasi, id_couple):
#     entity_type = data['entity_type'].lower()
#     value_type = data['value_type'].lower()
#     location = data['location'].lower()
#     template = ""
#     query = "SELECT id,template, couple FROM template WHERE entity_type='%s' AND value_type='%s'" % (entity_type, value_type)
    
#     if location == lokasi:
#         query += " AND (location = 'lokasi' OR location IS NULL)"
#     else:
#         query += " AND location IS NULL"

#     if "rank" in data:
#         rank = data['rank']
#         if rank > 1:
#             query += " AND (rank = '%d' OR rank IS NULL OR rank = '2-last')" % (rank)
#         else:
#             query += " AND (rank = '%d' OR rank IS NULL)" % (rank)
    
#     if id_couple != 0:
#         query1 = query + " AND id = %d" % (id_couple)
#         id_template, template, _ = templateRetrieval(query1)
#         couple = 0
    
#     query += " ORDER BY number_of_selection LIMIT 1"
#     if template == "":
#         id_template, template, couple = templateRetrieval(query)
   
#     return id_template, template, couple

def getTemplate(data, lokasi, id_couple):
    entity_type = data['entity_type'].lower()
    value_type = data['value_type'].lower()
    location = data['location'].lower()
    template = ""
    couple = 0
    query = "SELECT id,template, entity_type, value_type, couple, location, rank FROM template WHERE entity_type='%s' AND value_type='%s'" % (entity_type, value_type)
    if location == lokasi.lower():
        query += " AND (location = 'lokasi' OR location IS NULL)"
    else:
        query += " AND location IS NULL"

    if "rank" in data:
        rank = data['rank']
        if rank > 1:
            query += " AND (rank = '%d' OR rank IS NULL OR rank = '2-last')" % (rank)
        else:
            query += " AND (rank = '%d' OR rank IS NULL)" % (rank)
    
    if id_couple != 0:
        query1 = query + " AND id = %d" % (id_couple)
        template = templateRetrieval(query1)
        couple = 0
    
    query += " ORDER BY number_of_selection LIMIT 1"
    if not template:
        template = templateRetrieval(query)
        if "couple" in template:
            couple = template["couple"]
    return template, couple

def searchExistingTemplate(data, existingTemplates, couple):
    for template in existingTemplates:
        if template["value_type"].lower() == data["value_type"].lower() and template["entity_type"].lower() == data["entity_type"].lower() and template["prevlocation"] == data["location"] and ("rank" not in data or template["rank"] is None or template["rank"] == data["rank"]):
            if couple == 0:
                couple = template["couple"]
            else:
                couple = 0
            return template["id"], template["template"], couple
    return 0, "", couple
   
def getAggregationTemplate(data1, data2):
    id1 = data1["id_template"]
    id2 = data2["id_template"]
    query = "SELECT value_type1, template FROM aggregation_template WHERE (id1 = %d AND id2 = %d) OR (id1 = %d AND id2 = %d)" % (id1, id2, id2, id1)
    value_type, template = aggregationTemplateRetrieval(query)
    if value_type.lower() == data1["value_type"].lower():
        template = template.replace("{{value1}}", "{{value}}")
    else:
        template = template.replace("{{value2}}", "{{value}}")
    if id1 < id2:
        return str(id1) + ", " + str(id2), template
    else:
        return str(id2) + ", " + str(id1), template

def isValidContents(contents):
    count = 0
    for content in contents:
        if (content["id_template"] and "aggregated" not in content):
            count += 1
    if (count >= 2):
        return True
    else:
        return False
        
def mergeGroups(documentPlan, deprecatedContents):
    deprecatedContents = sorted(deprecatedContents)
    newGroup = []
    appendedContents = []
    for i in deprecatedContents:
        for j in range(0, len(documentPlan)):
            if i != j and j not in appendedContents and i not in appendedContents:
                for content in documentPlan[j]:
                    if documentPlan[i][0]["entity_type"] == content["entity_type"] and (documentPlan[i][0]["location_type"] == content["location_type"] or documentPlan[i][0]["value_type"] == content["value_type"]):
                        if (i < j):
                            newGroup.append((i,j))
                        else:
                            newGroup.append((j,i))
                        appendedContents.append(i)
                        appendedContents.append(j)
                        break
    newGroup = dict(sorted(newGroup))
    appendedContents = []
    newDocumentPlan = []
    for i in range(0, len(documentPlan)):
        if i not in appendedContents:
            if i in newGroup:
                newContent = documentPlan[i] + documentPlan[newGroup[i]]
                appendedContents.append(newGroup[i])
                newDocumentPlan.append(newContent)
            else:
                newDocumentPlan.append(documentPlan[i])
    return newDocumentPlan

def mergeGroups1(documentPlan, deprecatedContents):
    deprecatedContents = sorted(deprecatedContents)
    newGroup = []
    appendedContents = []
    for i in deprecatedContents:
        for j in range(0, len(documentPlan)):
            if i != j and j not in appendedContents and i not in appendedContents:
                for content in documentPlan[j]:
                    if documentPlan[i][0]["entity_type"] == content["entity_type"] or (documentPlan[i][0]["location_type"] == content["location_type"] or documentPlan[i][0]["value_type"] == content["value_type"]):
                        if (i < j):
                            newGroup.append((i,j))
                        else:
                            newGroup.append((j,i))
                        appendedContents.append(i)
                        appendedContents.append(j)
                        break
    newGroup = dict(sorted(newGroup))
    appendedContents = []
    newDocumentPlan = []
    for i in range(0, len(documentPlan)):
        if i not in appendedContents:
            if i in newGroup:
                newContent = documentPlan[i] + documentPlan[newGroup[i]]
                appendedContents.append(newGroup[i])
                newDocumentPlan.append(newContent)
            else:
                newDocumentPlan.append(documentPlan[i])
    return newDocumentPlan