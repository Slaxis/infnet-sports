from __future__ import annotations

from datetime import datetime

from pandas import read_csv

from ..stadium import Stadium
from ..teams.team import Team, TrueSkillTeam
from ..teams.teams import Teams
from .game import Game
from .result import Result
from .score import Score


class Games(dict[int, Game]):
    use_trueskill_teams : bool
    def __init__(self, game_dataframe_path : str = None, use_trueskill_teams : bool = False):
        super().__init__() # SUGESTÃO DO COPILOT GHAGHAAHA BOA COPILOT
        self.use_trueskill_teams = use_trueskill_teams
        if game_dataframe_path:
            self.load_games(game_dataframe_path) # SUGESTÃO DO COPILOT

    # SUGESTÃO DO COPILOT
    def load_games(self, game_dataframe_path : str):
        df = read_csv(game_dataframe_path)
        for ix, row in df.iterrows():
            game_id = row["ID"]
            game_round = row["rodata"]
            game_date_parts = row["data"].split("/")
            day, month, year = int(game_date_parts[0]), int(game_date_parts[1]), int(game_date_parts[2])
            game_hour_parts = row["hora"].split(":")
            day_hour, day_minutes = int(game_hour_parts[0]), int(game_hour_parts[1])
            hour = datetime(year, month, day, day_hour, day_minutes)
            home_name = row["mandante"].lower()
            away_name = row["visitante"].lower()

            if self.use_trueskill_teams:
                home = TrueSkillTeam(home_name)
                away = TrueSkillTeam(away_name)
            else:
                home = Team(home_name)
                away = Team(away_name)
            
            if row["vencedor"].lower() == home_name:
                winner = 1
            elif row["vencedor"].lower() == away_name:
                winner = -1
            else:
                winner = 0
            
            arena_name = row["arena"].lower()
            arena = Stadium(arena_name)
            score = Score(row["mandante_Placar"], row["visitante_Placar"])
            result = Result(winner, score)
            game = Game(game_id, game_round, hour, home, away, arena, result)
            self[game.id] = game

    @property
    def n_games(self):
        return len(self)
    
    @property
    def teams(self) -> Teams:
        teams = Teams()
        for game in self:
            home = self[game].home
            away = self[game].away
            if home not in teams:
                teams[home.name] = home
            if away not in teams:
                teams[away.name] = away
        return teams
    
    # SUGESTÃO DO COPILOT
    def get_games_until(self, day : datetime) -> Games:
        games_until = Games()
        for game in self:
            if self[game].hour <= day:
                games_until[game] = self[game] # SUGESTÃO DO COPILOT
        return games_until
    
    def get_teams_from_year(self, year = 2022) -> Teams:
        teams = Teams()
        for game in self:
            if self[game].hour.year == year:
                home = self[game].home
                away = self[game].away
                if home not in teams:
                    teams[home.name] = home
                if away not in teams:
                    teams[away.name] = away
        return teams