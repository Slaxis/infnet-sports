from datetime import datetime

from ..games.games import Games
from ..games.result import Result
from ..teams.team import Team
from ..teams.teams import Teams
from .ranker import Ranker
from scipy.stats import norm


class EloRanker(Ranker):
    starter_elo : float
    beta : float
    k_update : float

    def __init__(self, game_data_filepath : str, beta : float, starter_elo : float, k_update : float):
        super().__init__(game_data_filepath)
        self.beta = beta
        self.starter_elo = starter_elo
        self.k_update = k_update

        # instanciar todos os jogos
        self.games = Games(self.game_data_filepath)

    def create_ranking(self, ranking_day : datetime) -> list[Team]:
        print("COMEÇOU A RANKING")

        # instanciar todos os times
        self.teams = self.games.teams
        
        # setar o ELO inicial de todos os times
        for team in self.teams:
            self.teams[team].grade = self.starter_elo

        # pegar todos os jogos até o dia do ranking e atualizar os ELOs # SUGESTÃO DO COPILOT
        games_until_ranking_day = self.games.get_games_until(ranking_day) # SUGESTÃO DO COPILOT
        for game_id in games_until_ranking_day: # SUGESTÃO DO COPILOT
            game = self.games[game_id] # SUGESTÃO DO COPILOT
            home = self.teams[game.home.name]
            away = self.teams[game.away.name]
            new_home, new_away = self.update_grades(home, away, game.result) # SUGESTÃO DO COPILOT + AJUSTE
            self.teams[game.home.name] = new_home # SUGESTÃO DO COPILOT
            self.teams[game.away.name] = new_away # SUGESTÃO DO COPILOT
            # update the teams on game object
            game.home = Team(new_home.name, new_home.position, new_home.grade)
            game.away = Team(new_away.name, new_away.position, new_away.grade)
            self.games[game_id] = game

        # atualizar as posições de todos os times
        self.teams.update_positions()

        return self.teams.ranking

    # Pega os times e devolve o ELO atualizado
    def update_grades(self, home: Team, away: Team, result: Result) -> tuple[Team, Team]:

        # Calcular a probabilidade de vitória do time da casa
        home_prob = 1 - norm(loc=home.grade - away.grade, scale=2**(1/2)*self.beta).cdf(0)
        away_prob = 1 - home_prob
        true_home_prob = (result.winner + 1.0)/2.0
        true_away_prob = 1 - true_home_prob

        home_grade = home.grade
        away_grade = away.grade

        home.grade = self.k_update * (true_home_prob - home_prob) + home_grade
        away.grade = self.k_update * (true_away_prob - away_prob) + away_grade

        print(f"{home.name} ({home_grade:.0f}) x {away.name} ({away_grade:.0f}) winner: {result.winner} -> ({home.grade:.0f}) ({away.grade:.0f})")
        return home, away # SUGESTÃO DO COPILOT