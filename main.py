from flask import Flask, render_template, request
from model import focusRetrieval, yearRetrieval, levelRetrieval, locationRetrieval, cycleRetrieval, valueTypeRetrieval, entityRetrieval, subLocationRetrieval, getTimeAndLocation, templateDBInsertion
import json
from tkinter import *
from tkinter import filedialog

from src.automated_news_generator import automatedNewsGeneration

app = Flask(__name__)

@app.route('/news_generation', methods = ['GET'])
def queryInsertion():
	year = yearRetrieval()
	return render_template('news_generation.html', year = year)

@app.route('/template_insertion', methods = ['GET'])
def templateInsertion():
    return render_template('template_insertion.html')

@app.route('/getLevel', methods=['POST'])
def getLevel():
    year =  request.form['year']
    level = levelRetrieval(year)
    return json.dumps({'level':level});

@app.route('/getLocation', methods=['POST'])
def getLocation():
    year =  request.form['year']
    level =  request.form['level']
    location = locationRetrieval(year, level)
    return json.dumps({'loc':location});

@app.route('/getCycle', methods=['POST'])
def getCycle():
    year =  request.form['year']
    level =  request.form['level']
    location =  request.form['location']
    cycle = cycleRetrieval(year, level, location)
    return json.dumps({'cycle':cycle});

@app.route('/getFocus', methods=['POST'])
def getFocus():
    year =  request.form['year']
    level =  request.form['level']
    location =  request.form['location']
    cycle =  request.form['cycle']
    focus = focusRetrieval(year, level, location, cycle)
    return json.dumps({'focus':focus});

@app.route('/getFields', methods=['POST'])
def getFields():
    year =  request.form['year']
    level =  request.form['level']
    location =  request.form['location']
    cycle =  request.form['cycle']
    focus =  request.form['focus']
    value_type = valueTypeRetrieval(focus, year, level, location, cycle)
    entity = entityRetrieval(focus, year, level, location, cycle)
    sublocation = subLocationRetrieval(focus, year, level, location, cycle)
    return json.dumps({'entity':entity, 'sublocation': sublocation, 'value_type': value_type})

@app.route('/generateNews', methods=['POST'])
def generateNews():
    req = request.form
    req = req.to_dict(flat=False)
    article = automatedNewsGeneration(req)
    city, time = getTimeAndLocation()
    citytime = time + "\n\n"  + city + " - "
    return json.dumps({'article':article, 'citytime': citytime})

@app.route('/downloadNews', methods=['POST'])
def downloadNews():
    root = Tk()
    root.title("Save As")
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    root.destroy()
    article = request.form["article"]
    article = article.replace("<br>", "\n")
    article = article.replace("<b>", "")
    article = article.replace("</b>", "")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return json.dumps({"status": "error"})
    f.write(article)
    f.close() # `()` w 
    return json.dumps({"status": "ok"})

@app.route('/insertTemplate', methods=['POST'])
def insertTemplate():
    template =  request.form['template']
    value_type =  request.form['value_type']
    rank =  request.form['rank']
    focus =  request.form['entity_type']
    status = templateDBInsertion(template, value_type, rank, focus)
    return json.dumps({"status": status})

if __name__ == '__main__':
   app.run(debug = True)