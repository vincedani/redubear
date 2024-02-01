# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

class Reducer:
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_subparser(arg_parser) -> None:
        """
        If a reducer has additional arguments that would be nice to have, here, a subparser
        can be added to the main argument parser.
        """
        pass

    def generate_command(self, oracle, input_file, temp, stats) -> list[str]:
        raise NotImplementedError('Generate Command function is not implemented.')

    def post_process(self, stat_file, input_file, out_dir, temp_dir) -> dict:
        raise NotImplementedError('Post Process function is not implemented.')
