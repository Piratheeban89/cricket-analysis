from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from analysis import get_top_players_runs, get_top_players_avg, get_top_players_notout, get_top_highest_score, get_runs_per_ball, get_runs_per_innings
from webscraper import update_player_data
from analysis2 import get_strike_rate, get_centuries, get_fifties, get_no_sixes, get_no_fours
import requests 

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://mpratheep1989:Pira23mongoDB@cluster0.ogqxmcb.mongodb.net/?retryWrites=true&w=majority")
db = client["cricket_db"]
collection = db["player_data"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['GET', 'POST'])
def update_data():
    if request.method == 'POST':
        update_player_data()  # Call the update function
        return redirect(url_for('index'))

    return render_template('update.html')


@app.route('/top_players_runs')
def top_players_runs():
    top_players_runs_chart = get_top_players_runs(collection)
    return render_template('top_players_runs.html', top_players_runs=top_players_runs_chart)

@app.route('/top_players_avg')
def top_players_avg():
    top_players_avg_chart = get_top_players_avg(collection)
    return render_template('top_players_avg.html', top_players_avg=top_players_avg_chart)

@app.route('/top_players_notout')
def top_players_notout():
    top_players_notout_chart = get_top_players_notout(collection)
    return render_template('top_players_notout.html', top_players_notout=top_players_notout_chart)

@app.route('/top_players_highestscore')
def top_players_highestscore():
    top_players_highestscore_chart = get_top_highest_score(collection)
    return render_template('top_players_highestscore.html', top_players_highestscore=top_players_highestscore_chart)

@app.route('/top_hitters')
def top_hitters():
    top_hitters_chart = get_strike_rate(collection)
    return render_template('top_hitters.html', top_hitters=top_hitters_chart)    

@app.route('/top_centuries')
def top_centuries():
    top_centuries_chart = get_centuries(collection)
    return render_template('top_centuries.html', top_centuries=top_centuries_chart)  

@app.route('/top_fifties')
def top_fifties():
    top_fifties_chart = get_fifties(collection)
    return render_template('top_fifties.html', top_fifties=top_fifties_chart)

@app.route('/no_6s')
def no_6s():
    no_6s_chart = get_no_sixes(collection)
    return render_template('no_6s.html', no_6s=no_6s_chart)  

@app.route('/no_4s')
def no_4s():
    no_4s_chart = get_no_fours(collection)
    return render_template('no_4s.html', no_4s=no_4s_chart) 

@app.route('/runs_per_ball')
def runs_per_ball():
    runs_per_ball_chart = get_runs_per_ball(collection)
    return render_template('runs_per_ball.html', runs_per_ball=runs_per_ball_chart)  

@app.route('/runs_per_innings')
def runs_per_innings():
    runs_per_innings_chart = get_runs_per_innings(collection)
    return render_template('runs_per_innings.html', runs_per_innings=runs_per_innings_chart)  

if __name__ == '__main__':
    app.run(debug=True)
