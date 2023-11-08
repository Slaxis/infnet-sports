from datetime import datetime

from ..games.games import Games
from ..games.result import Result
from ..teams.team import Team
from ..teams.teams import Teams


class Ranker:
    game_data_filepath : str
    games : Games
    teams : Teams
    def __init__(self, game_data_filepath : str):
        self.game_data_filepath = game_data_filepath
    
    def create_ranking(self, ranking_day : datetime) -> Teams:
        pass

    def update_grades(home : Team, away : Team, result : Result):
        pass