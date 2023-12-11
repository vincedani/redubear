# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import cpu_count
from pathlib import Path

from redubear.utils import get_logger
from redubear.utils import process_path
from redubear.utils import ReducerRegistry
from redubear.utils import ReportGenerator
from redubear.benchmark import Tests, Benchmark

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tag',
                        required=True,
                        metavar='UNIQUE_TAG',
                        help='Measurement tag')

    parser.add_argument('-o', '--output',
                        type=lambda p: process_path(parser, p),
                        default=(Path() / 'experiments').resolve(),
                        metavar='OUTPUT_DIR',
                        help='Output directory where the reduced test cases are saved.')

    parser.add_argument('-w', '--workers',
                        type=int,
                        default=int(cpu_count() / 2),
                        choices=range(0, cpu_count()),
                        metavar=f'[0, {cpu_count()}]',
                        help='Number of workers to use to parallel reduce the tests')

    parser.add_argument('-m', '--memory',
                        default=False,
                        action='store_true',
                        help='Measure peak memory usage of the reducer excluding the SUT')

    parser.add_argument('--temp',
                        type=lambda p: process_path(parser, p),
                        default=Path('/tmp/reduction'),
                        metavar='TEMP_DIR',
                        help='Temporary directory where the reducers can save their intermediate files (will be deleted).')

    parser.add_argument('--log-level',
                        default='ERROR',
                        choices=['CRITICAL', 'FATAL', 'ERROR', 'WARN',
                                 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
                        help='Verbosity level of diagnostic messages')

    Tests.add_arguments(parser)

    subparsers = parser.add_subparsers(help='Available Reducers', dest='reducer')
    for reducer in ReducerRegistry.keys():
        ReducerRegistry.get(reducer).add_subparser(subparsers)

    args = parser.parse_args()
    return args


def main():
    """
    The CLI entry point of ReduBear.
    """
    args = parse_args()

    get_logger('ReduBear', log_level=args.log_level)

    benchmarks = Tests(args.benchmark, args.perses_root, args.jrts_root)
    reducer = ReducerRegistry.get(args.reducer)(**vars(args))

    executor = Benchmark(benchmarks, reducer, args.tag, args.workers, args.memory, args.output, args.temp)
    report = executor.run()

    report_file = args.output / f'ReduBear-{args.tag}.json'
    ReportGenerator.dump(report, report_file)
