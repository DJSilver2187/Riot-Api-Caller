from flask_cors import CORS
from flask import Flask
from flask import request
from flask import Response
import requests
import json

app = Flask(__name__)
CORS(app)

apiKey = "Enter Your Api Key"

@app.route('/')
def index():
    return "Hello World!"

@app.route('/getSummoner/<summoner>')
def getPuuid(summoner):
    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + 
                            summoner, headers={"X-Riot-Token" : apiKey})
    return response.json()

@app.route('/getMatchIds/<region>/<puuid>')
def getMatchIds(region, puuid):
    start = request.args.get("start")
    count = request.args.get("count")
    
    response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + 
                            "/ids?start=" + start + "&count=" + count, headers={"X-Riot-Token" : apiKey})
    return json.dumps(response.json())

@app.route('/getMatchInfo/<region>/<matchId>')
def getMatchInfo(region, matchId):
    response = requests.get("https://" + region + ".api.riotgames.com/lol/match/v5/matches/" + matchId, headers={"X-Riot-Token" : apiKey})
    if response.status_code == 200:
        return json.dumps(response.json())
    else:
        return Response("Unavailable", status=404, mimetype="text")
