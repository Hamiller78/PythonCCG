from pythonccg.card import Card
import random

class Zone:
    def __init__(self, name=None):
        self.name = name
        self.cards = []

    def add_to_top(self, card: Card):
        self.cards.insert(0, card)

    def add_to_bottom(self, card: Card):
        self.cards.append(card)

    def remove_from_top(self):
        if self.cards:
            return self.cards.pop(0)
        return None

    def remove_from_bottom(self):
        if self.cards:
            return self.cards.pop()
        return None

    def shuffle(self):
        random.shuffle(self.cards)

    def fill_from_file(self, filepath: str, cardpool):
        self.cards = []
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                card_name = line.strip()
                card = cardpool.create_card_by_name(card_name)
                if card:
                    self.add_to_bottom(card)
            self.shuffle()

    def clone(self):
        new_zone = Zone(self.name)
        new_zone.cards = [card.clone() for card in self.cards]
        return new_zone

    def __repr__(self):
        return f"Zone(cards={self.cards})"