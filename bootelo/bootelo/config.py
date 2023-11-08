import os
import sys
import json
WELCOME_TEXT = "Iniciando o BootElo..."

root_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_folder = os.path.join(root_folder, "data")
src_folder = os.path.join(root_folder, "src")
cfg_folder = os.path.join(src_folder, "cfg")
rankings_folder = os.path.join(src_folder, "rankings")

# processar os argvs
if len(sys.argv) != 5:
    print("Uso: python bootelo.py <cfg_ranker> <day> <month> <year>")
    exit(1)

cfg_ranker = sys.argv[1]

try:
    ranker_day = int(sys.argv[2])
    ranker_month = int(sys.argv[3])
    ranker_year = int(sys.argv[4])
except Exception as e:
    print("Erro: os argumentos de dia, mês e ano devem ser números inteiros.")
    exit(1)

# importar o json de configuração
try:
    config_filepath = os.path.join(cfg_folder, f"{cfg_ranker}.json")
    print(f"Importando configuração de {config_filepath}...")
    with open(config_filepath, "r") as f:
        cfg = json.load(f)

except Exception as e:
    print(f"Erro: não foi possível abrir o arquivo de configuração {cfg_ranker}.")
    exit(1)

try:
    game_data_filename = cfg["game_data_filename"]
    starter_elo = cfg["starter_elo"]
    beta = cfg["beta"]
    k_update = cfg["k_update"]
except Exception as e:
    print(f"Erro: não foi possível ler o arquivo de configuração {cfg_ranker}.")
    exit(1)

game_data_filepath = os.path.join(data_folder, game_data_filename)
csv_export_filepath = os.path.join(rankings_folder, f"{cfg_ranker}_{ranker_year}_{ranker_month}_{ranker_day}.csv")

print(f"CONFIG {cfg_ranker} ENCONTRADA! valores: {game_data_filename}, {starter_elo}, {beta}, {k_update}, {ranker_day}, {ranker_month}, {ranker_year}")
