# app.py
import mysql.connector
# Import the Flask module
from flask import Flask, request, render_template
import csv
import re

# Import the MySQL module to interact with our MySQL database
# from flaskext.mysql import MySQL

#from flask_mysqldb import MySQL

import os
import sys

# Create a Flask application instance
app = Flask(__name__)

sqlhost = os.environ.get('MYSQL_HOST')
sqluser = os.environ.get('MYSQL_USER')
sqlpassword = os.environ.get('MYSQL_PASSWORD')
sqldb = os.environ.get('MYSQL_DATABASE')

app.config.from_mapping(
    MYSQL_HOST=sqlhost,
    MYSQL_USER=sqluser,
    MYSQL_PASSWORD=sqlpassword,
    MYSQL_DB=sqldb
)


mydb = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)



@app.route("/")
def index():

    dossier = "static/logos"
    teams = []
    for nom_fichier in sorted(os.listdir(dossier)):
        teams.append(nom_fichier[:3])

    return render_template('index.html', teams=teams)


@app.route("/team")
def players():

    team = request.args.get('team')

    cur = mydb.cursor()
    query = f"SELECT * FROM players NATURAL JOIN rosters WHERE team = '{team}'"
    cur.execute(query)
    players = cur.fetchall()

    return render_template('basketball.html', players=players,team = team)

@app.route("/addplayer", methods=['GET','POST'])
def addplayer():

    team = request.args.get('team')

    if request.method == 'POST':
        cur = mydb.cursor()
        # cur = mysql.connection.cursor()
        # cur.execute(query)
        query = "SELECT MAX(id) FROM players"
        cur.execute(query)
        id = cur.fetchall()[0][0] + 1

        nom = request.form['nom']
        number = request.form['number']
        position = request.form['position']
        height = request.form['height']
        weight = request.form['weight']
        birthdate = request.form['birthdate']
        country = request.form['country']
        experience = request.form['experience']
        college = request.form['college']
        team = request.form['team']
        print(team)

        query = f"INSERT INTO players(id, number, name, position, height, weight, birthdate, country, exp, college) VALUES({id},{number},'{nom}', '{position}', '{height}', {weight}, '{birthdate}', '{country}', '{experience}', '{college}')"
        cur.execute(query)
        query = f"INSERT INTO rosters(id,team) VALUES({id},'{team}')"
        cur.execute(query)
        mydb.commit()
        return "Le formulaire a été soumis avec succès"
    else:
        return render_template('addplayer.html',team=team)


# Start the Flask application if this file is being executed as the main script
if __name__ == "__main__":
    # Start the Flask application, listening on all available interfaces
    dic = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07",
       "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

    cur = mydb.cursor()

    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    tablesAlreadyExists = False

    for tab in tables:
        if(tab[0]=="players"): tablesAlreadyExists = True
    
    if(not tablesAlreadyExists):

        cur.execute("CREATE TABLE IF NOT EXISTS players(id INT PRIMARY KEY, number INT, name VARCHAR(100), position VARCHAR(2), height VARCHAR(4), weight INT, birthdate DATE, country VARCHAR(2), exp VARCHAR(2), college VARCHAR(100))")
        cur.execute("CREATE TABLE IF NOT EXISTS rosters(id INT PRIMARY KEY, team VARCHAR(3), FOREIGN KEY (id) REFERENCES players(id))")

        with open('static/csv/players.csv', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                expression = re.compile(r',')
                row[6] = expression.sub('', row[6])
                addzero = False
                if (row[6][-7] == ' '): addzero = True
                if (addzero):
                    gooddate = str(row[6][-4:]) + '-' + dic.get(row[6][:-7:]) + '-0' + str(row[6][-6])
                else:
                    gooddate = str(row[6][-4:]) + '-' + dic.get(row[6][:-8:]) + '-' + str(row[6][-7:-5])
                
                row[6] = gooddate
                
                # 2,3,4,6,7,8,9
                for i in [2,3,4,6,7,8,9]:
                    row[i] = '"' + row[i] + '"'
        
                query = "INSERT INTO players(id, number, name, position, height, weight, birthdate, country, exp, college) VALUES(" + ','.join(row) + ");"
                cur.execute(query)
                cur = mydb.cursor()
            
        mydb.commit()
        with open('static/csv/rosters.csv', encoding='utf-8', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            for row in reader:
                row[1] = '"' + row[1] + '"'
                query = "INSERT INTO rosters(id, team) VALUES(" + ','.join(row) + ");"
                cur.execute(query)
        mydb.commit()
    app.run(debug=True, host="0.0.0.0")