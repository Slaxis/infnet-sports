class Common:
    name : str
    def __init__(self, name : str):
        self.name = name.lower()

    def __repr__(self) -> str:
        return self.name