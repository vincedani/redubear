# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from os import cpu_count
from pathlib import Path

from redubear.reducers import Reducer
from redubear.utils import ReducerRegistry


@ReducerRegistry.register('picire')
class Picire(Reducer):

    @staticmethod
    def add_subparser(arg_parser) -> None:
        parser = arg_parser.add_parser(
            'picire', help='Arguments for Picire reducer')

        parser.add_argument('--atom',
                            choices=['char', 'line', 'both'],
                            default='line',
                            help='atom (i.e., granularity) of input')

        parser.add_argument('--dd-star',
                            default=False,
                            action='store_true',
                            help='use fixpoint iteration of DDMin')
        Picire._common_arguments(parser)

    @staticmethod
    def _common_arguments(parser) -> None:
        parallel_parser = parser.add_argument_group('Parallel Options')
        parallel_parser.add_argument('-p', '--parallel',
                                     action='store_true',
                                     default=False,
                                     help='run DD in parallel')
        parallel_parser.add_argument('-j', '--jobs',
                                     metavar='N',
                                     type=int,
                                     default=cpu_count(),
                                     help='maximum number of test commands to execute in parallel (has effect in parallel mode only; default: %(default)s)')

        # Cache related options.
        cache_parser = parser.add_argument_group('Cache Options')
        cache_parser.add_argument('--cache',
                                  metavar='NAME',
                                  choices=['config', 'config-tuple',
                                           'content', 'content-hash', 'none'],
                                  default='config',
                                  help='cache strategy (%(choices)s; default: %(default)s)')
        cache_parser.add_argument('--cache-fail',
                                  action='store_true',
                                  default=False,
                                  help='store failing, i.e., interesting test cases in the cache')
        cache_parser.add_argument('--no-cache-evict-after-fail',
                                  dest='evict_after_fail',
                                  action='store_false',
                                  default=True,
                                  help='disable the eviction of larger test cases from the cache when a failing, i.e., interesting test case is found')

    def __init__(self,
                 atom: str,
                 dd_star: bool,
                 cache: str,
                 cache_fail: bool,
                 evict_after_fail: bool,
                 parallel: bool,
                 jobs: int,
                 **kwargs) -> None:
        self.atom = atom
        self.dd_star = dd_star
        self.cache = cache
        self.cache_fail = cache_fail
        self.evict_after_fail = evict_after_fail
        self.parallel = parallel
        self.jobs = jobs

    def unique_id(self) -> str:
        return f'picire-{self.atom}-{self.dd_star}-{self.cache}-{self.cache_fail}-{self.evict_after_fail}-{self.parallel}-{self.jobs}'

    def generate_command(self, oracle: Path, input_file: Path, temp: Path, output: Path, stats: Path) -> list[str]:
        command = [
            'picire',
            '--log-level', 'ERROR',
            '--complement-first',
            '--subset-iterator', 'skip',
            '--complement-iterator', 'backward',
            '--cache', self.cache,
            '--atom', self.atom,
            '--test', str(oracle),
            '--input', str(input_file),
            '--out', str(temp),
            '--statistics', str(stats),
        ]

        if not self.dd_star:
            command.extend(['--no-dd-star'])

        if not self.evict_after_fail:
            command.extend(['--no-cache-evict-after-fail'])

        if self.cache_fail:
            command.extend(['--cache-fail'])

        if self.parallel:
            command.extend(['--parallel'])
            command.extend(['--jobs', '4'])

        return command
