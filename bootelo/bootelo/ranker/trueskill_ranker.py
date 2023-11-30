from datetime import datetime

from ..games.games import Games
from ..games.result import Result
from ..teams.team import Team, TrueSkillTeam
from ..teams.teams import Teams
from .ranker import Ranker
from scipy.stats import norm
from trueskill import TrueSkill


class TrueskillRanker(Ranker):
    trueskill_env : TrueSkill
    def __init__(self, game_data_filepath : str, mu=25.0, sigma=8.333333333333334, beta=4.166666666666667, tau=0.08333333333333334, draw_probability=0.1):
        super().__init__(game_data_filepath)
        self.trueskill_env = TrueSkill(mu, sigma, beta, tau, draw_probability)

        # instanciar todos os jogos
        self.games = Games(self.game_data_filepath, use_trueskill_teams=True)

    def create_ranking(self, ranking_day : datetime) -> list[Team]:
        print("COMEÇOU A RANKING")

        # instanciar todos os times
        self.teams = self.games.teams
        
        # setar o ELO inicial de todos os times
        for team in self.teams:
            self.teams[team].rating = self.trueskill_env.create_rating()

        # pegar todos os jogos até o dia do ranking e atualizar os ELOs # SUGESTÃO DO COPILOT
        games_until_ranking_day = self.games.get_games_until(ranking_day) # SUGESTÃO DO COPILOT
        for game_id in games_until_ranking_day: # SUGESTÃO DO COPILOT
            game = self.games[game_id] # SUGESTÃO DO COPILOT
            home = self.teams[game.home.name]
            away = self.teams[game.away.name]
            new_home, new_away = self.update_grades(home, away, game.result) # SUGESTÃO DO COPILOT + AJUSTE
            self.teams[game.home.name] = new_home # SUGESTÃO DO COPILOT
            self.teams[game.away.name] = new_away # SUGESTÃO DO COPILOT

        # atualizar as posições de todos os times
        self.teams.update_positions()
        return self.teams.ranking

    # Pega os times e devolve o ELO atualizado
    def update_grades(self, home: TrueSkillTeam, away: TrueSkillTeam, result: Result) -> tuple[Team, Team]:
        home_rating = home.rating
        away_rating = away.rating

        new_home_rating, new_away_rating = self.trueskill_env.rate_1vs1(home_rating, away_rating, drawn=result.winner == 0)

        home.rating = new_home_rating
        away.rating = new_away_rating

        print(f"{home.name} ({home_rating}) x {away.name} ({away_rating}) winner: {result.winner} -> ({home.rating}) ({away.rating})")
        return home, away # SUGESTÃO DO COPILOT