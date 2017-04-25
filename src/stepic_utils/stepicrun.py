#!/usr/bin/env python3

import sys
import argparse
import random
import unittest

from stepic_utils import utils
from stepic_utils.quiz import DatasetQuiz, CodeQuiz, StringQuiz

GENERATE_COMMAND = 'generate'
SCORE_COMMAND = 'score'
SOLVE_COMMAND = 'solve'
TEST_COMMAND = 'test'
SAMPLE_COMMAND = 'sample'

DATASET_QUIZ = 'dataset'
CODE_QUIZ = 'code'
STRING_QUIZ = 'string'


class Runner(object):
    """
    Runs user code and deals with encodings
    """
    def __init__(self, quiz, seed=None):
        self.seed = seed

        self.encode = utils.encode
        self.decode = utils.decode

        self.quiz = quiz

    def generate(self):
        assert self.seed, "seed should be specified explicitly"
        random.seed(self.seed)
        dataset_clue = self.quiz.generate()
        return self.encode(dataset_clue)

    def score(self, data):
        reply, clue = self.decode(data)
        result = self.quiz.check(reply, clue)
        return self.encode(result)

    def solve(self, data):
        dataset = self.decode(data)
        reply = self.quiz.solve(dataset)
        return self.encode(reply)

    def sample(self):
        return self.encode(self.quiz.sample)


def read_bin_stdin():
    binary_input = sys.stdin.buffer.read()
    return binary_input


def write_bin_stdout(data):
    sys.stdout.buffer.write(data)


def main():
    parser = argparse.ArgumentParser(description='Test or run python exercise')
    parser.add_argument('-c', '--command', required=True,
                        choices=[GENERATE_COMMAND, SCORE_COMMAND, SOLVE_COMMAND, TEST_COMMAND,
                                 SAMPLE_COMMAND])
    parser.add_argument('-p', '--code-path', default='user_code.py')
    parser.add_argument('-s', '--seed', type=int)
    parser.add_argument('-t', '--type', default=DATASET_QUIZ, choices=[DATASET_QUIZ, CODE_QUIZ, STRING_QUIZ])
    args = parser.parse_args()
    print(args.type)
    if args.type == DATASET_QUIZ:
        quiz_class = DatasetQuiz
    elif args.type == CODE_QUIZ:
        quiz_class = CodeQuiz
    elif args.type == STRING_QUIZ:
        quiz_class = StringQuiz
    else:
        assert False

    quiz = quiz_class.import_quiz(args.code_path)
    runner = Runner(quiz, seed=args.seed)

    if args.command == GENERATE_COMMAND:
        if not args.seed:
            print('error: seed should be specified for generate command')
            sys.exit()

        # printing binary data in compatible way
        generated = runner.generate()
        sys.stdout.buffer.write(generated)

    elif args.command == SCORE_COMMAND:
        binary_input = read_bin_stdin()
        scored = runner.score(binary_input)
        write_bin_stdout(scored)
    elif args.command == SOLVE_COMMAND:
        binary_input = read_bin_stdin()
        solved = runner.solve(binary_input)
        write_bin_stdout(solved)
    elif args.command == TEST_COMMAND:
        unittest.main(testLoader=quiz_class.get_test_loader(),
                      module=quiz.module, argv=[sys.argv[0]])
    elif args.command == SAMPLE_COMMAND:
        sample = runner.sample()
        sys.stdout.buffer.write(sample)
    else:
        assert False, 'unknown command'

if __name__ == '__main__':
    main()
