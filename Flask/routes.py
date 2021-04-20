from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teams')
def teams():
    return render_template('teams-main.html')


@app.route('/standings', methods=("POST", "GET"))
def pl_standings():
    standings = main.get_live_Standings()
    topScorers = main.getTopScorer()
    return render_template('standings.html', tables=[standings.to_html(classes='allfix')],titles=standings.columns.values,
                           scorers=[topScorers.to_html(classes='allfix')], scorerTitles=topScorers.columns.values)


@app.route('/results', methods=("POST", "GET"))
def pl_results(week='1'):
    standings = main.getAllFixtures(week)
    return render_template('results.html', tables=[standings.to_html(classes='allfix')],
                           titles=standings.columns.values)


@app.route('/results/week=<string:week>', methods=("POST", "GET"))
def pl_results_by_week(week='1'):
    standings = main.getAllFixtures(week)
    return render_template('results.html', tables=[standings.to_html(classes='allfix')],
                           titles=standings.columns.values)


@app.route('/contact', methods=("POST", "GET"))
def contact():
    return render_template('contact.html')


@app.route('/teams/<string:team>', methods=("POST", "GET"))
def team_table(team='spurs'):
    team_results = main.getAllCompResults(team)
    record_transfers = main.getTeamTransfers(team)
    roster = main.getTeamRosters(team)
    return render_template('teams.html', tables=[team_results.to_html(classes='allfix')],
                           titles=team_results.columns.values,
                           transfers=[record_transfers.to_html(classes='allfix')],
                           transferTitles = record_transfers.columns.values,
                           rosters=[roster.to_html(classes='allfix')],
                           rosterTitles=roster.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
