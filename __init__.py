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

import requests
from flask import render_template, jsonify

@app.route('/commits/')
def index():
    # URL de l'API GitHub pour le repository (modifie cette URL selon ton repo)
    repo_api_url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    
    # Effectue une requête GET pour récupérer la liste des commits
    response = requests.get(repo_api_url)
    
    # Vérification que la requête est réussie (status code 200)
    if response.status_code == 200:
        commits_data = response.json()  # Parse les données JSON
        
        # On peut ici extraire des informations spécifiques sur chaque commit
        commits_list = []
        for commit in commits_data:
            commit_info = {
                'message': commit['commit']['message'],
                'author': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date']
            }
            commits_list.append(commit_info)
        
        # Passe les commits extraits au template HTML
        return render_template('commits.html', commits=commits_list)
    else:
        return jsonify({"error": "Unable to fetch commits from GitHub"}), 500

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})

if __name__ == "__main__":
  app.run(debug=True)
