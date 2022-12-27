import unittest
from unittest import mock

from predict_message import predict_message_mood


class TestPredictModel(unittest.TestCase):

    def test_mock_predict(self):
        tests_val = [
            (0, "неуд"),
            (0.29, "неуд"),
            (0.3, "норм"),
            (0.8, "норм"),
            (0.81, "отл"),
            (1, "отл")
        ]
        with mock.patch('predict_message.SomeModel') as mock_model:
            mock_model.predict.side_effect = [val[0] for val in tests_val]
            for line, val in tests_val:
                res = predict_message_mood(line, mock_model)
                self.assertEqual(res, val)
            self.assertEqual(mock_model.predict.call_count, len(tests_val))
            for i, arg in enumerate(mock_model.predict.mock_calls):
                self.assertEqual(arg.args[0], tests_val[i][0])

    def test_predict_lamda(self):
        tests_val = [
            ("", "неуд"),
            ("qww`z ./,l[-['123", "неуд"),
            ("qww`zчяк ./,вфьдлвааl[-['123`zxc", "норм"),
            ("qw.,l[-13", "отл")
        ]
        with mock.patch('predict_message.SomeModel') as mock_model:
            mock_model.predict.side_effect = lambda x: len(x) / (10 ** len(str(len(x))))
            for line, val in tests_val:
                res = predict_message_mood(line, mock_model)
                self.assertEqual(res, val)
            self.assertEqual(mock_model.predict.call_count, len(tests_val))
            for i, arg in enumerate(mock_model.predict.mock_calls):
                self.assertEqual(arg.args[0], tests_val[i][0])

    def test_predict_change_coef(self):
        tests_val = [
            ("qww`z ./,l[-['123", "норм", 0.0, 0.3),
            ("qww`z ./,l[-['123", "неуд", 0.2, 0.3),
            ("qww`z ./,l[-['123", "отл", 0.0, 0.1),
            ("qww`z ./,l[-['123", "отл", 0.1, 0.1),
            ("qww`z ./,l[-['123", "отл", 0.15, 0.1),
        ]

        with mock.patch('predict_message.SomeModel') as mock_model:
            mock_model.predict.side_effect = lambda x: len(x) / (10 ** len(str(len(x))))
            for line, val, bad_coef, good_coef in tests_val:
                res = predict_message_mood(line, mock_model, bad_thresholds=bad_coef, good_thresholds=good_coef)
                self.assertEqual(res, val)
            self.assertEqual(mock_model.predict.call_count, len(tests_val))
            for i, arg in enumerate(mock_model.predict.mock_calls):
                self.assertEqual(arg.args[0], tests_val[i][0])
