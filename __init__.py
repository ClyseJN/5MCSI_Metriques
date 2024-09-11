from flask import Flask, render_template_string, render_template, jsonify
from flask import json
from datetime import datetime
from urllib.request import urlopen
import requests  # Ajout de requests pour l'API GitHub
import sqlite3

app = Flask(__name__)

# Page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Page de contact
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

# Récupérer les données météo et les renvoyer en JSON
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# API pour récupérer les commits minute par minute sur GitHub
@app.route('/commits/')
def get_commits():
    GITHUB_USER = 'ton-utilisateur-github'  # Remplace par ton nom d'utilisateur GitHub
    GITHUB_REPO = 'ton-repo-github'         # Remplace par ton dépôt GitHub

    url = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits'
    response = requests.get(url)

    if response.status_code == 200:
        commits = response.json()
        commit_count_by_minute = {}

        # Transformation des données des commits minute par minute
        for commit in commits:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            minute = commit_date.strftime("%H:%M")
            if minute in commit_count_by_minute:
                commit_count_by_minute[minute] += 1
            else:
                commit_count_by_minute[minute] = 1

        return jsonify(commit_count_by_minute)
    else:
        return jsonify({'error': 'Impossible de récupérer les commits'})

# Page pour le graphique
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Page pour l'histogramme
@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

if __name__ == "__main__":
  app.run(debug=True)
