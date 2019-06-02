# -*- coding: utf-8 -*-
import argparse
from abc import abstractmethod
from argparse import ArgumentTypeError

from pre_commit_logic.util.check_failed_exception import CheckFailedException


class CheckerTemplateMethod(object):
    def __init__(self, argv):
        self.parser = argparse.ArgumentParser()
        self._add_arguments_to_parser()
        self.args = self.parser.parse_args(argv)
        self._check_arguments()

    def _add_arguments_to_parser(self):
        pass

    def _check_arguments(self):
        pass

    def run(self):
        """Prepare args and then check locations."""
        try:
            self._perform_checks()
            return 0
        except ArgumentTypeError as ex:
            print ex.message
            return 1
        except CheckFailedException as ex:
            print ex.message
            return 2

    @abstractmethod
    def _perform_checks(self):
        pass

    def inform_check_failure(self, message):
        raise CheckFailedException(message)

    def check_arguments_size_match(self, arguments_one, arguments_two):
        if not arguments_one:
            arguments_one = []
        if not arguments_two:
            arguments_two = []
        if len(arguments_one) != len(arguments_two):
            self.inform_check_failure('Las listas de argumentos no tienen el mismo largo.')
