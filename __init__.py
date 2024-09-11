from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

@app.route("/extract-minutes/<date_string>")
def extract_minutes(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
    except ValueError as e:
        return jsonify({'error': 'Invalid date format'}), 400

@app.route("/commits/")
def github_commits():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        response = urlopen(url)
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))

        commit_dates = []
        for commit in json_content:
            date_string = commit.get('commit', {}).get('author', {}).get('date')
            if date_string:
                commit_dates.append(date_string)
        
        return jsonify({'commit_dates': commit_dates})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
  app.run(debug=True)
