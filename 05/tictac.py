class TicTac:

    def __init__(self, player1="Player1", player2="Player2"):
        self.player1 = player1
        self.player2 = player2
        self.cur_player = self.player1

        self.__is_game_end = False
        self.__game_field = []
        for _ in range(3):
            self.__game_field.append([None] * 3)

    def start_game(self):
        print('game_start')
        while not self.__is_game_end:
            self.make_step()
        print('game end')

    def __is_free_pos(self, pos):
        return self.__game_field[pos // 3][pos % 3] is None

    def __is_field_full(self):
        return not any(None in line for line in self.__game_field)

    def make_step(self):
        if self.__is_game_end:
            print("Game end")
            return None

        print(f'this {self.cur_player}`s step')
        print('enter num from 0 - 8')
        step = input()

        try:
            step = self.validate_input(step)
        except ValueError as err:
            print(err.args[0])
        else:
            if self.__is_free_pos(step):
                self.__game_field[step // 3][step % 3] = bool(self.cur_player is self.player1)

                self.show_board()

                winner = self.check_winner()
                if winner is not None:
                    print(f"winner is {self.cur_player}")
                    self.__is_game_end = True
                    return None

                if self.__is_field_full():
                    print("the game is tied")
                    self.__is_game_end = True
                    return None

                self.cur_player = self.player2 if self.cur_player is self.player1 else self.player1

            else:
                print('this position is busy')
                return None
        return None

    def __check_list_for_win(self, check_win_lists):
        for cur_list in check_win_lists:
            if None not in cur_list:
                if all(cur_list):
                    return self.player1

                if not any(cur_list):
                    return self.player2
        return None

    def check_winner(self):
        trans_field = list(zip(*self.__game_field))
        for i, val in enumerate(self.__game_field):
            res = self.__check_list_for_win([val, trans_field[i]])
            if res is not None:
                return res

        main_diag = [self.__game_field[j][j] for j in range(len(self.__game_field))]
        another_diag = [self.__game_field[-(j + 1)][j] for j in range(len(self.__game_field))]
        return self.__check_list_for_win([main_diag, another_diag])

    def show_board(self):
        print('------------------------')
        for line in self.__game_field:
            for val in line:
                if val is None:
                    print('.\t', end=' ')
                elif val:
                    print('x\t', end=' ')
                else:
                    print('o\t', end=' ')
            print()
        print('------------------------')
        return self.__game_field.copy()

    def validate_input(self, value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError as exc:
                raise ValueError('value must be digits') from exc

        if isinstance(value, int):
            if 0 > value or value > 8:
                raise ValueError('value must be in range 0-8')
            return int(value)

        raise ValueError('value must be digits')


if __name__ == "__main__":
    cur_game = TicTac()
    cur_game.start_game()
