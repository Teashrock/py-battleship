class Deck:
    def __init__(self, row: int, column: int, is_alive:bool=True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start, end, is_drowned=False) -> None:
        # Create decks and save them to a list `self.decks`
        self.decks: list[Deck] = []
        self.is_drowned = is_drowned
        # One-deck ship
        if start == end:
            self.decks = [Deck(*start)]
        else:
            start_row    = start[0]
            start_column = start[1]
            end_row      = end[0]
            end_column   = end[1]
            self.decks = [
                Deck(row, column)
                for row in range(start_row, end_row + 1)
                for column in range(start_column, end_column + 1)
            ]

    def get_deck(self, row, column) -> Deck | None:
        # Find the corresponding deck in the list
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row, column):
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        fired_deck = self.get_deck(row, column)
        fired_deck.is_alive = False
        self.is_drowned = not all(deck for deck in self.decks)
        if self.is_drowned:
            return "Sunk!"
        else:
            return "Hit!"


class Battleship:
    def __init__(self, ships: list[tuple[tuple, tuple]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        #self.field: dict[tuple, Ship] = {ship: Ship(ship[0], ship[1]) for ship in ships}
        self.field: dict[tuple, Ship] = {}
        for ship in ships:
            present_points = []
            start = ship[0]
            end   = ship[1]
            if start[0] != end[0]:
                present_points = [(x, end[1]) for x in range(start[0], end[0] + 1)]
            elif start[1] != end[1]:
                present_points = [(start[0], y) for y in range(start[1], end[1] + 1)]
            else:
                present_points = ship[0]
            self.field[tuple(present_points)] = Ship(ship[0], ship[1])
        print(self.field)

    def fire(self, location: tuple):
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location)
        if ship is not None:
            return ship.fire(*location)
        else:
            return "Miss!"
