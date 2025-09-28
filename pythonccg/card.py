class Card:
    def __init__(self, id: int, name: str, cost: int, attack: int, health: int, is_ready: bool = False):
        self.id = id
        self.name = name
        self.cost = cost
        self.attack = attack
        self.health = health
        self.is_ready = is_ready

    def __repr__(self):
        return (f"Card(id={self.id}, name='{self.name}', cost={self.cost}, "
            f"attack={self.attack}, health={self.health}, is_ready={self.is_ready})")

    def clone(self):
        return Card(self.id, self.name, self.cost, self.attack, self.health, self.is_ready)