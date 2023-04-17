from random import randint


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self._n = 3
        self.pole = tuple(tuple(Cell() for _ in range(self._n)) for _ in range(self._n))
        self._win = 0

    def __index_validator(self, indx):
        if type(indx) not in (list, tuple) or len(indx) != 2:
            raise IndexError('некорректно указанные индексы')
        r, c = indx
        if not (0 <= r < self._n) or not (0 <= c < self._n):
            raise IndexError('некорректно указанные индексы')

    def __win_updater(self):
        for row in self.pole:
            if all(x.value == self.HUMAN_X for x in row):
                self._win = 1
                return
            if all(x.value == self.COMPUTER_O for x in row):
                self._win = 2
                return

        for i in range(self._n):
            if all(x.value == self.HUMAN_X for x in (row[i] for row in self.pole)):
                self._win = 1
                return
            if all(x.value == self.COMPUTER_O for x in (row[i] for row in self.pole)):
                self._win = 2
                return

        if all(self.pole[i][i].value == self.HUMAN_X for i in range(self._n)) or \
                all(self.pole[i][-1 - i].value == self.HUMAN_X for i in range(self._n)):
            self._win = 1
            return
        if all(self.pole[i][i].value == self.COMPUTER_O for i in range(self._n)) or \
                all(self.pole[i][-1 - i].value == self.COMPUTER_O for i in range(self._n)):
            self._win = 2
            return

        if all(x.value == self.FREE_CELL for row in self.pole for x in row):
            self._win = 3
            return

    def __getitem__(self, item):
        self.__index_validator(item)
        r, c = item
        return self.pole[r][c].value

    def __setitem__(self, key, value):
        self.__index_validator(key)
        r, c = key
        self.pole[r][c].value = value
        self.__win_updater()

    def init(self):
        for row in range(self._n):
            for x in range(self._n):
                self.pole[row][x].value = 0
        self._win = 0

    def show(self):
        for row in self.pole:
            for j in row:
                print(j.value, end=" ")
            print()
        print("----------------------------------")

    def human_go(self):
        if not self:
            return

        while True:
            r, c = list(map(int, input("Введите координаты свободной клетки: ").split()))
            self.__index_validator((r, c))
            if not (0 < r <= self._n) or not (0 < c <= self._n):
                continue
            if self[r, c] == self.FREE_CELL:
                self[r, c] = self.HUMAN_X
                break

    def computer_go(self):
        if not self:
            return

        while True:
            r = randint(0, self._n - 1)
            c = randint(0, self._n - 1)
            self.__index_validator((r, c))
            if self[r, c] != self.FREE_CELL:
                continue

            self[r, c] = self.COMPUTER_O
            break

    @property
    def is_human_win(self):
        return self._win == 1

    @property
    def is_computer_win(self):
        return self._win == 2

    @property
    def is_draw(self):
        return self._win == 3

    def __bool__(self):
        return self._win == 0 and self._win not in (1, 2, 3)


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")