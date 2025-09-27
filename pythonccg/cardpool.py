import csv
from .card import Card

class Cardpool:
    _next_id = 0

    def load_from_csv(self, filepath: str):
        self.cards = []
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                card = Card(
                    id=None,
                    name=row[0],
                    cost=int(row[1]),
                    attack=int(row[2]),
                    health=int(row[3])
                )
                self.cards.append(card)

    def create_card_by_name(self, name: str):
        for card in self.cards:
            if card.name == name:
                new_card = card.clone()
                new_card.id = self._id()
                return new_card
        return None

    def _id(self):
        id = Cardpool._next_id
        Cardpool._next_id += 1
        return id
