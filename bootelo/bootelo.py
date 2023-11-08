from datetime import datetime
from pandas import DataFrame

from bootelo.config import (WELCOME_TEXT, beta, game_data_filepath, k_update,
                            ranker_day, ranker_month, ranker_year, starter_elo, csv_export_filepath)
from bootelo.ranker.elo_ranker import EloRanker

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    print(WELCOME_TEXT)
    ranker = EloRanker(game_data_filepath, beta, starter_elo, k_update=k_update)
    team_list = ranker.create_ranking(datetime(ranker_year, ranker_month, ranker_day))

    # save the ranking
    team_tuples = []
    for team in team_list:
        team_tuples.append((team.name, team.position, team.grade))
    
    df_teams = DataFrame(team_tuples, columns=['team', 'position', 'grade'])
    df_teams.to_csv(csv_export_filepath, index=False, sep=';', decimal=',')