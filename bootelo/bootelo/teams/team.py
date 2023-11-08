from ..common import Common

class Team(Common):
    position : int
    grade : float

    def __init__(self, name : str):
        super().__init__(name)
        self.position = 0
        self.grade = 0.0

    def __repr__(self):
        return f"{self.name}: {self.position}º @ {self.grade:.0f}"