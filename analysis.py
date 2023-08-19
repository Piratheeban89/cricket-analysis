import matplotlib.pyplot as plt
import io
import base64
from flask import Markup
from pymongo.collection import Collection
import numpy as np

def generate_chart(chart_data, x_labels, y_labels, title, color):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(x_labels, y_labels, color=color)
    plt.xlabel('Players')
    plt.ylabel(chart_data)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    for bar, label in zip(bars, y_labels):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label, ha='center', va='bottom')


    # Save the chart to a BytesIO object
    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format="png")
    plt.close()
    chart_stream.seek(0)

    # Convert the chart image to base64-encoded string
    chart_base64 = base64.b64encode(chart_stream.read()).decode('utf-8')

    chart_html = f'<img src="data:image/png;base64,{chart_base64}">'
    return Markup(chart_html)

def get_top_players_runs(collection: Collection):
    top_players = collection.find().sort("runs", -1).limit(10)

    player_names = []
    player_runs = []

    for player in top_players:
        player_names.append(player["name"])
        player_runs.append(player["runs"])

    return generate_chart("Runs", player_names, player_runs, "Top 10 Players with Highest Runs", "blue")

def get_top_players_avg(collection: Collection):
    top_avg_players = collection.find().sort("average", -1).limit(10)

    player_names = []
    player_average = []

    for player in top_avg_players:
        player_names.append(player["name"])
        player_average.append(player["average"])

    return generate_chart("Batting Average", player_names, player_average, "Top 10 Batsmen with Highest Batting Averages", "green")

def get_top_players_notout(collection: Collection):
    top_players_notout = collection.find().sort("not_outs", -1).limit(10)
    
    player_names =[]
    player_notout= []
    
    for player in top_players_notout:
        player_names.append(player["name"])
        player_notout.append(player["not_outs"])
        
    return generate_chart("Not Outs", player_names, player_notout, "Top 10 Batsman with Highest Number of Not Outs", "Orange" )

def get_top_highest_score(collection: Collection):
    top_highest_score = collection.find().sort("highest_score", -1).limit(10)

    player_names = []
    player_highestscore = []
    
    for player in top_highest_score:
        player_names.append(player["name"])
        player_highestscore.append(player["highest_score"])
        
    return generate_chart("highest_score", player_names, player_highestscore, "Top 10 Batsman with Highest Score", "Blue" )
    

def get_runs_per_ball(collection: Collection):
    runs = collection.find().sort("runs", -1).limit(10)
    balls = collection.find().sort("balls_faced", -1).limit(10)
    
    player_runs_per_ball = []

    for run_doc, ball_doc in zip(runs, balls):
        player_name = run_doc["name"]
        runs_scored = run_doc["runs"]
        balls_faced = ball_doc["balls_faced"]

        if balls_faced == 0:
            runs_per_ball = 0
        else:
            runs_per_ball = runs_scored / balls_faced
        
        runs_per_ball = round(runs_per_ball, 2)

        player_runs_per_ball.append((player_name, runs_per_ball))
        
        player_runs_per_ball.sort(key=lambda x: x[1], reverse=True)

    player_names = [player[0] for player in player_runs_per_ball]
    runs_per_ball_values = [player[1] for player in player_runs_per_ball]

    return generate_chart("Runs per Ball", player_names, runs_per_ball_values, "Top 10 Batsmen - Runs per Ball", "Blue")

def get_runs_per_innings(collection: Collection):
    runs = collection.find().sort("runs", -1).limit(10)
    innings = collection.find().sort("innings", -1).limit(10)
    
    player_runs_per_innings = []

    for run_doc, innings_doc in zip(runs, innings):
        player_name = run_doc["name"]
        runs_scored = run_doc["runs"]
        innings_faced = innings_doc["innings"]

        if innings_faced == 0:
            runs_per_ball = 0
        else:
            runs_per_ball = runs_scored / innings_faced
        
        runs_per_ball = round(runs_per_ball, 2)

        player_runs_per_innings.append((player_name, runs_per_ball))
        
        player_runs_per_innings.sort(key=lambda x: x[1], reverse=True)

    player_names = [player[0] for player in player_runs_per_innings]
    runs_per_innings_values = [player[1] for player in player_runs_per_innings]

    return generate_chart("Average Runs per Innings", player_names, runs_per_innings_values, "Top 10 Batsmans with Hihgest Average Runs per Innings", "Blue")