from contextlib import contextmanager
from io import StringIO, BytesIO
from unittest import TestCase
from unittest.mock import patch

from ..stepicrun import main
from ..utils import decode


class BaseTest(TestCase):
    @contextmanager
    def assert_fail_with_message(self, expected_message):
        fake_stderr = StringIO()
        with patch('sys.stderr', fake_stderr):
            with self.assertRaises(SystemExit):
                yield
        stderr = fake_stderr.getvalue()
        self.assertEqual(stderr, expected_message)

    def assert_run_result(self, args, expected_result):
        fake_buffer = BytesIO()
        with patch('sys.stdout') as mock_stdout:
            mock_stdout.buffer = fake_buffer
            main(args=args)
        result = decode(fake_buffer.getvalue())
        self.assertEqual(result, expected_result)
