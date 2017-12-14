from .utils import BaseTest


class RunTest(BaseTest):
    def test_has_solve_true(self):
        args = ('-t', 'code', '-p', 'code/generate_datasets.py', '-c', 'has_solve')

        self.assert_run_result(args, True)

    def test_has_solve_false(self):
        args = ('-t', 'code', '-p', 'code/generate_datasets_without_solve.py', '-c', 'has_solve')

        self.assert_run_result(args, False)
