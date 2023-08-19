from bs4 import BeautifulSoup
import requests 
from pymongo import MongoClient

def update_player_data():
    client = MongoClient("mongodb+srv://mpratheep1989:Pira23mongoDB@cluster0.ogqxmcb.mongodb.net/?retryWrites=true&w=majority")
    db = client["cricket_db"]
    collection = db["player_data"]
    
    collection.delete_many({})
    
    url = 'https://www.espncricinfo.com/records/most-runs-in-career-282827'
    source = requests.get(url)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')
    players = soup.find('tbody').find_all('tr')
    
    for player in players:
        name = player.find('a', class_='ds-inline-flex ds-items-start ds-leading-none').text
        country_start = name.rfind('(') + 1
        country_end = name.rfind(')')
        country = name[country_start:country_end]
        other_data = player.find_all('td')
        span = other_data[1].text
        matches = int(other_data[2].text)
        innings = int(other_data[3].text)
        not_outs = int(other_data[4].text)
        runs = int(other_data[5].text)
        high_score = other_data[6].text.strip('*')
        highest_score = int(high_score)
        average = float(other_data[7].text)
        balls_faced = int(other_data[8].text)
        strike_rate = float(other_data[9].text)
        centuries_text = other_data[10].text
        centuries = int(centuries_text) if centuries_text != '-' else 0
        fifties = int(other_data[11].text)
        ducks_text = other_data[12].text
        ducks = int(ducks_text) if ducks_text != '-' else 0
        no_4s = int(other_data[13].text)
        no_6s = int(other_data[14].text)

        data = {
            "name": name,
            "country": country,
            "span": span,
            "matches": matches,
            "innings": innings,
            "not_outs": not_outs,
            "runs": runs,
            "highest_score": highest_score,
            "average": average,
            "balls_faced": balls_faced,
            "strike_rate": strike_rate,
            "centuries": centuries,
            "fifties": fifties,
            "ducks": ducks,
            "no_fours": no_4s,
            "no_sixes": no_6s
        }

        collection.insert_one(data)
