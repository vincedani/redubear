# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import json
import picire
import stat

# Time tracking
import time
from datetime import date, timedelta

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from os import chmod, cpu_count, environ, makedirs
from pathlib import Path
from shutil import copy2, rmtree
from subprocess import Popen, PIPE
from string import Template

from redubear.utils import get_logger
from redubear.utils import process_path
from redubear.utils import Benchmarks
from redubear.utils import ReducerRegistry

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--tag',
                        required=True,
                        metavar='UNIQUE_TAG',
                        help='Measurement tag')

    parser.add_argument('-r', '--report',
                        required=True,
                        type=lambda p: process_path(parser, p),
                        metavar='MEASUREMENT_REPORT.json',
                        help='Path to save the final measurement report in JSON format.')

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

    parser.add_argument('--log-level',
                        default='ERROR',
                        choices=['CRITICAL', 'FATAL', 'ERROR', 'WARN',
                                 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
                        help='Verbosity level of diagnostic messages')

    Benchmarks.add_arguments(parser)

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
    benchmarks = Benchmarks(args.benchmark, args.perses_root, args.jrts_root)

    for test_name, oracle, input_file in benchmarks:
        print(test_name, oracle, input_file)

