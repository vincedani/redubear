# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from pathlib import Path
from argparse import SUPPRESS

from redubear.reducers import Picire
from redubear.reducers.grammars import get_grammar
from redubear.utils import ReducerRegistry


@ReducerRegistry.register('picireny')
class Picireny(Picire):

    @staticmethod
    def add_subparser(arg_parser) -> None:
        parser = arg_parser.add_parser('picireny', help='Arguments for Picireny reducer')

        Picire._common_arguments(parser)

        # Suppress --atom in Picireny as it is unused in HDD.
        parser.add_argument('--atom', help=SUPPRESS)

        hdd_parser = parser.add_argument_group('HDD Options')
        hdd_parser.add_argument('--hdd',
                                metavar='NAME',
                                choices=['hdd', 'hddr'],
                                default='hdd',
                                help='HDD variant to run (%(choices)s; default: %(default)s)')

        hdd_parser.add_argument('--phase',
                                metavar='NAME',
                                choices=['prune', 'coarse-prune', 'hoist', 'prune+hoist', 'coarse-prune+hoist'],
                                action='append',
                                help='parametrization of the HDD variant to run (%(choices)s; default: prune) '
                                     '(may be specified multiple times to run different parametrization in sequence)')

    def __init__(self,
                 dd_star: bool,
                 greeddy: bool,
                 cache: str,
                 cache_fail: bool,
                 evict_after_fail: bool,
                 jobs: int,
                 hdd: str,
                 phase: list,
                 measure_memory: bool,
                 **kwargs) -> None:
        super().__init__(None, dd_star, greeddy, cache, cache_fail, evict_after_fail, jobs, measure_memory)
        self.hdd = hdd
        self.phases = phase

    def generate_command(self, oracle: Path, input_file: Path, temp: Path, stats: Path) -> list[str]:
        grammar, start_rule = get_grammar(input_file.suffix[1:])

        command = [
           'picireny',
            '--sys-recursion-limit', '10000',
            '--flatten-recursion',
            '--start', start_rule,
            '--hdd', self.hdd,
            '--grammar',
        ]
        command += grammar

        for phase in self.phases:
            command += ['--phase', phase]

        command += self._common_parts(oracle, input_file, temp, stats)

        return command
