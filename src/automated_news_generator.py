# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:42:21 2018

@author: Steffi Indrayani
"""

from src.document_planning import documentPlanning
from src.microplanning import microplanning
from src.input_handler import readQuery
from src.realisation import realisation

import json
#from microplanning import lexicalisation

# def main():
#     article = automatedNewsGeneration()
#     writeToFile(article)
    
def automatedNewsGeneration(request):    
    query, request = readQuery(request)
    documentPlan = documentPlanning(query, request)
    if (len(documentPlan) == 0):
        print("NEWS CAN'T BE GENERATED DUE TO DATA NOT AVAILABLE")
        return ""
    textSpecification = microplanning(documentPlan, request)
    with open("results/dictionary", 'w', encoding="utf-8") as outfile:
        json.dump(textSpecification, outfile, ensure_ascii=False)
    article = realisation(textSpecification)
    return article
    
# def writeToFile(article):    
#     city = "Bandung"
#     time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')
    
#     filename = "../results/article.txt" 
    
#     f = open(filename,'w')
#     f.write(time)
#     f.write("\n\n")
#     f.write(city + " - " + article)
#     f.close()