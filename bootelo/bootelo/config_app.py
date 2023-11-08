import json
import os
from datetime import datetime

from bootelo.ranker.elo_ranker import EloRanker
from flask import Flask, render_template
from pandas import DataFrame

WELCOME_TEXT = "Welcome to Bootelo!"
CFG_RANKER = "booteloapp"

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")
cfg_folder = os.path.join(src_folder, "cfg")

# importar o json de configuração
try:
    config_filepath = os.path.join(cfg_folder, f"{CFG_RANKER}.json")
    print(f"Importando configuração de {config_filepath}...")
    with open(config_filepath, "r") as f:
        cfg = json.load(f)

except Exception as e:
    print(f"Erro: não foi possível abrir o arquivo de configuração {CFG_RANKER}.")
    exit(1)

# importar as configurações
# "game_data_filename" : "campeonato-brasileiro-full.csv",
# "starter_elo" : 600,
# "beta" : 200,
# "k_update" : 5

try:
    game_data_filename = cfg["game_data_filename"]
    game_data_filepath = os.path.join(data_folder, game_data_filename)
    starter_elo = cfg["starter_elo"]
    beta = cfg["beta"]
    k_update = cfg["k_update"]
except Exception as e:
    print(f"Erro: configuração inválida arquivo {CFG_RANKER}.")
    exit(1)

ranker = EloRanker(game_data_filepath, beta, starter_elo, k_update)

app = Flask(__name__, static_folder='static', template_folder='templates'
            )

@app.route("/")
def home():
    return f"<h1>{WELCOME_TEXT}</h1><br><p>Ranking Beta: <br>{ranker.beta}</p><br><p>Ranking Starter Elo: <br>{ranker.starter_elo}</p><br><p>Ranking K Update: <br>{ranker.k_update}</p>"

@app.route("/ranking/<ranker_day_str>/<ranker_month_str>/<ranker_year_str>")
def ranking(ranker_day_str : str, ranker_month_str : str, ranker_year_str:str):
    ranker_day = int(ranker_day_str)
    ranker_month = int(ranker_month_str)
    ranker_year = int(ranker_year_str)

    try:
        team_list = ranker.create_ranking(datetime(ranker_year, ranker_month, ranker_day))

        # save the ranking
        team_tuples = []
        for team in team_list:
            team_tuples.append((team.name, team.position, team.grade))
        
        df_teams = DataFrame(team_tuples, columns=['team', 'position', 'grade'])
    except Exception as e:
        return f"<p>Erro: {e}</p>"

    leaderboard = df_teams.to_dict('records')
    return render_template('home.jinja2', leaderboard=leaderboard)