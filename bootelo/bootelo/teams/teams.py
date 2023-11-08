from .team import Team

class Teams(dict[str, Team]):

    def update_positions(self):
        teams = sorted(self.values(), key=lambda team: team.grade, reverse=True)
        for i, team in enumerate(teams):
            team.position = i + 1
    
    @property
    def ranking(self) -> list[Team]:
        return sorted(self.values(), key=lambda team: team.position, reverse=False)