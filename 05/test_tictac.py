import unittest
from unittest import mock
from tictac import TicTac


class TestTicTac(unittest.TestCase):

    @mock.patch("builtins.input")
    def test_input(self, mock_input):
        """
        test input validation and step operation
        test busy cell
        :param mock_input: mock input function
        :return: assert result
        """
        cur_game = TicTac()

        def _test_input(input_data, expected_str):
            for cur_val in input_data:
                self.assertRaises(ValueError, cur_game.validate_input, cur_val)
                mock_input.return_value = cur_val
                with mock.patch('builtins.print') as mock_print:
                    cur_game.make_step()
                    mock_print.assert_called_with(expected_str)

        _test_input(input_data=["fwdfw", [12, 4, 2], "4.6"], expected_str="value must be digits")
        _test_input(input_data=["-1", "9", "1000"], expected_str='value must be in range 0-8')

        local_steps_lists = [[3, 3], [1, 2, 2, 2, 1, 3], [8, 3, 2, 5, 2, 2]]
        for local_steps in local_steps_lists:
            cur_game = TicTac()
            mock_input.side_effect = local_steps
            for i, val in enumerate(local_steps):
                if local_steps.index(val) < i:
                    with mock.patch('builtins.print') as mock_print:
                        cur_game.make_step()
                        mock_print.assert_called_with('this position is busy')
                else:
                    cur_game.make_step()

    @mock.patch("builtins.input")
    def test_win(self, mock_input):
        """
        test variant of win for each player
        :param mock_input: mock input function
        :return: asserts result
        """
        steps_for_win = [
            [0, 4, 1, 5, 2, 6],  # 1 line win
            [3, 0, 4, 1, 5, 8],  # 2 line win
            [6, 0, 7, 2, 8, 5],  # 3 line win
            [0, 2, 3, 7, 6, 5],  # 1 column win
            [1, 3, 4, 6, 7, 8],  # 2 column win
            [2, 0, 5, 1, 8, 3],  # 3 column win
            [0, 1, 4, 2, 8, 3],  # main diag win
            [6, 3, 4, 5, 2, 1]  # add diag win
        ]

        def _test_win(is_second_win=False):
            for cur_steps in steps_for_win:
                cur_game = TicTac()
                mock_input.side_effect = cur_steps[::(-1) ** int(is_second_win)]
                for _ in range(len(cur_steps) - (1 + int(not is_second_win))):
                    cur_game.make_step()

                with mock.patch('builtins.print') as mock_print:
                    cur_game.make_step()
                    mock_print.assert_called_with(
                        f"winner is {cur_game.player2 if is_second_win else cur_game.player1}")
                    cur_game.make_step()
                    mock_print.assert_called_with("Game end")

        _test_win(False)
        _test_win(True)

        tie_game = [1, 0, 4, 2, 5, 3, 6, 7, 8]  # tie game
        cur_game = TicTac()
        mock_input.side_effect = tie_game
        for _ in range(len(tie_game) - 1):
            cur_game.make_step()

        with mock.patch('builtins.print') as mock_print:
            cur_game.make_step()
            mock_print.assert_called_with("the game is tied")
            cur_game.make_step()
            mock_print.assert_called_with("Game end")
