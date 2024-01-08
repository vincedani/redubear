# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from pathlib import Path

from redubear.reducers import Picire
from redubear.reducers.grammars import get_grammar
from redubear.utils import ReducerRegistry


@ReducerRegistry.register('picireny')
class Picireny(Picire):

    @staticmethod
    def add_subparser(arg_parser) -> None:
        parser = arg_parser.add_parser('picireny', help='Arguments for Picireny reducer')

        Picire._common_arguments(parser)

    def __init__(self,
                 dd_star: bool,
                 cache: str,
                 cache_fail: bool,
                 evict_after_fail: bool,
                 parallel: bool,
                 jobs: int,
                 **kwargs) -> None:
        super().__init__(None, dd_star, cache, cache_fail, evict_after_fail, parallel, jobs)

    def generate_command(self, oracle: Path, input_file: Path, temp: Path, stats: Path) -> list[str]:
        grammar, start_rule = get_grammar(input_file.suffix[1:])

        command = [
           'picireny',
            '--sys-recursion-limit', '10000',
            '--flatten-recursion',
            '--start', start_rule,
            '--grammar',
        ]
        command += grammar

        command += self._common_parts(oracle, input_file, temp, stats)
        return command


