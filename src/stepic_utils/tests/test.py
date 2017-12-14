import os
import textwrap

from io import StringIO
from contextlib import contextmanager
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec
from unittest import TestCase
from unittest.mock import patch

from stepic_utils.quiz import check_signatures
from ..quiz import CodeQuiz, DatasetQuiz, StringQuiz


class BaseTest(TestCase):
    @contextmanager
    def assert_fail_with_message(self, expected_message):
        fake_stderr = StringIO()
        with patch('sys.stderr', fake_stderr):
            with self.assertRaises(SystemExit):
                yield
            stderr = fake_stderr.getvalue()
            self.assertEqual(stderr, expected_message,
                             "Expected: {}\nGot: {}".format(expected_message, stderr))


def get_quiz(name=None, code=None, quiz_cls=DatasetQuiz):
    if name is not None:
        examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
        path = os.path.join(examples_dir, name)
        return quiz_cls.import_quiz(path)
    if code is not None:
        quiz_module = module_from_spec(ModuleSpec('quiz', None))
        exec(code, {}, quiz_module.__dict__)
        return quiz_cls.import_quiz(quiz_module)


# noinspection PyTypeChecker
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

    def test_self_check_success(self):
        for name in ['string_quiz_with_solve.py', 'string_quiz_without_solve.py']:
            quiz = get_quiz(name, quiz_cls=StringQuiz)
            self.assertTrue(quiz.self_check())

    def test_self_check_fail(self):
        quiz = get_quiz('string_quiz_with_solve_fail.py', quiz_cls=StringQuiz)
        self.assertFalse(quiz.self_check())


class CheckSignatureTest(BaseTest):
    def test_valid(self):
        specs = [('f', lambda: None, 0),
                 ('f', lambda *args: None, 0),
                 ('f', lambda x: None, 1),
                 ('f', lambda *args: None, 1),
                 ('f', lambda x, *args: None, 1),
                 ('f', lambda x, y: None, 2),
                 ('f', lambda *args: None, 2),
                 ('f', lambda x, *args: None, 2),
                 ('f', lambda x, y, *args: None, 2)]

        self.assertIsNone(check_signatures(specs))

    def test_wrong_number_of_args_1_expected(self):
        invalid_funcs = [
            lambda: None,
            lambda x, y: None,
            lambda x, y, z: None,
        ]
        for f in invalid_funcs:
            specs = [('f', f, 1)]

            with self.assert_fail_with_message("`f` should accept 1 argument.\n"):
                check_signatures(specs)

    def test_wrong_number_of_args_2_expected(self):
        invalid_funcs = [
            lambda: None,
            lambda x: None,
            lambda x, y, z: None,
        ]
        for f in invalid_funcs:
            specs = [('f', f, 2)]

            with self.assert_fail_with_message("`f` should accept 2 arguments.\n"):
                check_signatures(specs)


# noinspection PyTypeChecker
class CodeQuizTest(BaseTest):
    def test_generate_required(self):
        expected_msg = ("Can't import 'generate' from the challenge module.\n"
                        "It should export 'generate', 'check' functions.\n")

        with self.assert_fail_with_message(expected_msg):
            get_quiz(code="", quiz_cls=CodeQuiz)

    def test_check_required(self):
        code = textwrap.dedent("""
            def generate():
                return []
            """)
        expected_msg = ("Can't import 'check' from the challenge module.\n"
                        "It should export 'generate', 'check' functions.\n")

        with self.assert_fail_with_message(expected_msg):
            get_quiz(code=code, quiz_cls=CodeQuiz)

    def test_generate_datasets(self):
        quiz = get_quiz('code/generate_datasets.py', quiz_cls=CodeQuiz)

        tests = quiz.generate()

        self.assertEqual(tests, [('2 2\n', '4'), ('5 7\n', '12')])

    def test_generate_tuples(self):
        quiz = get_quiz('code/generate_tuples.py', quiz_cls=CodeQuiz)

        tests = quiz.generate()

        self.assertEqual(tests, [('2 2\n', 'clue:4'), ('5 7\n', 'clue:12')])

    def test_generate_datasets_without_solve(self):
        quiz = get_quiz('code/generate_datasets_without_solve.py', quiz_cls=CodeQuiz)

        tests = quiz.generate()

        self.assertEqual(tests, [('2 2\n', None), ('5 7\n', None)])

    def test_generate_tuples_without_solve(self):
        quiz = get_quiz('code/generate_tuples_without_solve.py', quiz_cls=CodeQuiz)

        tests = quiz.generate()

        self.assertEqual(tests, [('2 2\n', 'clue:4'), ('5 7\n', 'clue:12')])

    def test_self_check_success(self):
        for name in ['code/generate_datasets.py',
                     'code/generate_tuples.py']:
            quiz = get_quiz(name, quiz_cls=CodeQuiz)

            self.assertTrue(quiz.self_check())

    def test_self_check_without_solve_success(self):
        for name in ['code/generate_datasets_without_solve.py',
                     'code/generate_tuples_without_solve.py']:
            quiz = get_quiz(name, quiz_cls=CodeQuiz)

            self.assertTrue(quiz.self_check())
