import os

from unittest import TestCase

from ..quiz import CodeQuiz, DatasetQuiz


def get_quiz(name, quiz_cls=DatasetQuiz):
    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
    path = os.path.join(examples_dir, name)
    return quiz_cls.import_quiz(path)


class ExamplesTest(TestCase):
    def test_ab(self):
        quiz = get_quiz('ab.py')
        dataset, clue = quiz.generate()
        self.assertIn('file', dataset)

    def test_ab_dict(self):
        quiz = get_quiz('ab_dict.py')
        dataset, clue = quiz.generate()
        self.assertNotIn('file', dataset)

    def test_hints(self):
        quiz = get_quiz('hints.py')
        self.assertIn('bigger', quiz.check('32', '')[1])
        self.assertIn('smaller', quiz.check('52', '')[1])
        self.assertEqual(quiz.check('42', '')[0], 1)

    def test_all(self):
        for name in ['ab.py', 'ab_dict.py', 'divisors.py', 'hints.py', 'even_numbers.py', 'fib.py']:
            quiz = get_quiz(name)
            self.assertTrue(quiz.self_check(), "{} failed".format(name))

    def test_float(self):
        quiz = get_quiz('ab_float.py')
        dataset, clue = quiz.generate()
        self.assertIn('file', dataset)

    def test_score_rounding(self):
        quiz = get_quiz('rounding_errors.py')
        self.assertTrue(quiz.check('1', '1')[0])
        self.assertFalse(quiz.check('1', '2')[0])

    def test_dataset_generate_auto_append_new_line(self):
        for quiz_filename in ['ab.py', 'ab_newlined.py']:
            quiz = get_quiz(quiz_filename)

            dataset, clue = quiz.generate()

            self.assertTrue(dataset['file'].endswith('\n'))
            self.assertEqual(len(dataset['file']), 4)

    def test_code_generate_auto_append_new_line(self):
        for quiz_filename in ['code_ab.py', 'code_ab_newlined.py']:
            quiz = get_quiz(quiz_filename, quiz_cls=CodeQuiz)

            tests = quiz.generate()

            self.assertEqual(len(tests), 10)
            for dataset, clue in tests:
                self.assertTrue(dataset.endswith('\n'))
                self.assertEqual(len(dataset), 4)
