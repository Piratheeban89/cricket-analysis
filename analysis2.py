import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from pymongo.collection import Collection
from flask import Markup


def generate_chart(chart_data, x_labels, y_labels, title, color):
    plt.figure(figsize=(10, 6))
    bars = plt.barh(y_labels, x_labels, color=color)
    plt.xlabel(chart_data)
    plt.ylabel('Players')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    for bar, label in zip(bars, x_labels):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, label, va='center', ha='left')


    # Save the chart to a BytesIO object
    chart_stream = io.BytesIO()
    plt.savefig(chart_stream, format="png")
    plt.close()
    chart_stream.seek(0)

    # Convert the chart image to base64-encoded string
    chart_base64 = base64.b64encode(chart_stream.read()).decode('utf-8')

    chart_html = f'<img src="data:image/png;base64,{chart_base64}">'
    return Markup(chart_html)

def get_strike_rate(collection: Collection):
    strike_rate = collection.find().sort("strike_rate", -1).limit(10)

    player_names = []
    player_strike = []

    for player in strike_rate:
        player_names.append(player["name"])
        player_strike.append(player["strike_rate"])
        
    player_names.reverse()
    player_strike.reverse()

    return generate_chart("Strike Rate", player_strike, player_names, "Top 10 Players with Highest Stike Rate", "blue")

def get_centuries(collection: Collection):
    centuries = collection.find().sort("centuries", -1).limit(10)

    player_names = []
    player_centuries = []

    for player in centuries:
        player_names.append(player["name"])
        player_centuries.append(player["centuries"])
        
    player_names.reverse()
    player_centuries.reverse()

    return generate_chart("Number of Centuries", player_centuries, player_names, "Top 10 Players with High Number of Centuries", "blue")

def get_fifties(collection: Collection):
    fifties = collection.find().sort("fifties", -1).limit(10)

    player_names = []
    player_fifties = []

    for player in fifties:
        player_names.append(player["name"])
        player_fifties.append(player["fifties"])
        
    player_names.reverse()
    player_fifties.reverse()

    return generate_chart("Number of Fifties", player_fifties, player_names, "Top 10 Players with High Number of Fifties", "blue")

def get_no_sixes(collection: Collection):
    no_sixes = collection.find().sort("no_sixes", -1).limit(10)

    player_names = []
    player_sixes = []

    for player in no_sixes:
        player_names.append(player["name"])
        player_sixes.append(player["no_sixes"])
        
    player_names.reverse()
    player_sixes.reverse()

    return generate_chart("Number of Sixes ", player_sixes, player_names, "Top 10 Six Hitters", "Green")

def get_no_fours(collection: Collection):
    no_fours = collection.find().sort("no_fours", -1).limit(10)

    player_names = []
    player_fours = []

    for player in no_fours:
        player_names.append(player["name"])
        player_fours.append(player["no_fours"])
        
    player_names.reverse()
    player_fours.reverse()

    return generate_chart("Number of Fours ", player_fours, player_names, "Top 10 Four Hitters", "Green")