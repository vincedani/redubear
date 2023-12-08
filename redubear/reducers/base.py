# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from pathlib import Path

class Reducer:
    def __init__(self, oracle: Path, input: Path, output: Path) -> None:
        self.oracle = oracle
        self.input = input
        self.output = output

    @staticmethod
    def add_subparser(arg_parser) -> None:
        """
        If a reducer has additional arguments that would be nice to have, here, a subparser
        can be added to the main argument parser.
        """
        pass

    def reduce(**kwargs):
        pass
