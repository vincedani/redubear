# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from os import cpu_count

from redubear.reducers import Reducer
from redubear.utils import ReducerRegistry


@ReducerRegistry.register('picire')
class Picire(Reducer):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
    def _common_arguments(parser) ->None:
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

    def reduce(self, **kwargs):
        pass
