from datetime import datetime

from ..stadium import Stadium
from ..teams.team import Team
from .result import Result


class Game:
    id : int
    round : int
    hour : datetime
    home : Team
    away : Team
    arena : Stadium
    result : Result

    def __init__(self, id : int, round : int, hour : datetime, home : Team, away : Team, arena : Stadium, result : Result):
        self.id = id
        self.round = round
        self.hour = hour
        self.home = home
        self.away = away
        self.arena = arena
        self.result = result

    def __repr__(self):
        return f"{self.arena}, {self.home} X {self.away}"
