# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from pathlib import Path
from redubear.utils import process_path

BENCHMARKS = {
    # JerryScript Reduction Test Suite (https://github.com/vincedani/jrts)
    'jerry-3299': ['jrts', 'test.sh', '3299-orig.js'],
    'jerry-3361': ['jrts', 'test.sh', '3361-orig.js'],
    'jerry-3376': ['jrts', 'test.sh', '3376-orig.js'],
    'jerry-3408': ['jrts', 'test.sh', '3408-orig.js'],
    'jerry-3431': ['jrts', 'test.sh', '3431-orig.js'],
    'jerry-3433': ['jrts', 'test.sh', '3433-orig.js'],
    'jerry-3437': ['jrts', 'test.sh', '3437-orig.js'],
    'jerry-3479': ['jrts', 'test.sh', '3479-orig.js'],
    'jerry-3483': ['jrts', 'test.sh', '3483-orig.js'],
    'jerry-3506': ['jrts', 'test.sh', '3506-orig.js'],
    'jerry-3523': ['jrts', 'test.sh', '3523-orig.js'],
    'jerry-3534': ['jrts', 'test.sh', '3534-orig.js'],
    'jerry-3536': ['jrts', 'test.sh', '3536-orig.js'],

    # Perses Test Suite (https://github.com/uw-pluverse/perses)
    # Note that the docker environment from the linked repository must be set up.
    'clang-18556': ['perses', 'r.sh', 'small.c'],
    'clang-18596': ['perses', 'r.sh', 'small.c'],
    'clang-19595': ['perses', 'r.sh', 'small.c'],
    'clang-20680': ['perses', 'r.sh', 'small.c'],
    'clang-21467': ['perses', 'r.sh', 'small.c'],
    'clang-21582': ['perses', 'r.sh', 'small.c'],
    'clang-22337': ['perses', 'r.sh', 'small.c'],
    'clang-22382': ['perses', 'r.sh', 'small.c'],
    'clang-22704': ['perses', 'r.sh', 'small.c'],
    'clang-23309': ['perses', 'r.sh', 'small.c'],
    'clang-23353': ['perses', 'r.sh', 'small.c'],
    'clang-25900': ['perses', 'r.sh', 'small.c'],
    'clang-26350': ['perses', 'r.sh', 'small.c'],
    'clang-26760': ['perses', 'r.sh', 'small.c'],
    'clang-27137': ['perses', 'r.sh', 'small.c'],
    'clang-27747': ['perses', 'r.sh', 'small.c'],
    'clang-31259': ['perses', 'r.sh', 'small.c'],

    # Perses Test Suite (https://github.com/uw-pluverse/perses)
    # Note that the docker environment from the linked repository must be set up.
    'gcc-58731': ['perses', 'r.sh', 'small.c'],
    'gcc-59903': ['perses', 'r.sh', 'small.c'],
    'gcc-60116': ['perses', 'r.sh', 'small.c'],
    'gcc-60452': ['perses', 'r.sh', 'small.c'],
    'gcc-61047': ['perses', 'r.sh', 'small.c'],
    'gcc-61383': ['perses', 'r.sh', 'small.c'],
    'gcc-61917': ['perses', 'r.sh', 'small.c'],
    'gcc-64990': ['perses', 'r.sh', 'small.c'],
    'gcc-65383': ['perses', 'r.sh', 'small.c'],
    'gcc-66186': ['perses', 'r.sh', 'small.c'],
    'gcc-66375': ['perses', 'r.sh', 'small.c'],
    'gcc-66412': ['perses', 'r.sh', 'small.c'],
    'gcc-66691': ['perses', 'r.sh', 'small.c'],
    'gcc-70127': ['perses', 'r.sh', 'small.c'],
    'gcc-70586': ['perses', 'r.sh', 'small.c'],
    'gcc-71626': ['perses', 'r.sh', 'small.c'],
}


class Tests:

    @staticmethod
    def add_arguments(parser) -> None:
        benchmark_parser = parser.add_argument_group('Benchmark Options')

        benchmark_parser.add_argument('--jrts-root',
                                      type=lambda p: process_path(parser, p, should_exist=True),
                                      default=None,
                                      help='Home directory of JerryScript Reduction Test Suite (<path/to/project>/tests)')

        benchmark_parser.add_argument('--perses-root',
                                      type=lambda p: process_path(parser, p, should_exist=True),
                                      default=None,
                                      help='Home directory of Perses Test Suite (<path/to/project>/benchmark)')

        benchmark_parser.add_argument('--benchmark',
                                      choices=['jerry', 'clang', 'gcc'] + list(BENCHMARKS.keys()),
                                      default=None,
                                      help='Test case to be reduced. "jerry", "clang", "gcc": whole test suite.')

        benchmark_parser.add_argument('--custom-oracle',
                                      type=lambda p: process_path(parser, p, should_exist=True),
                                      default=None,
                                      help='Custom oracle script for "--custom-input". Omits --benchmark arguments.')

        benchmark_parser.add_argument('--custom-input',
                                      type=lambda p: process_path(parser, p, should_exist=True),
                                      default=None,
                                      help='Custom input file to be reduced. Omits --benchmark arguments.')

    def __init__(self,
                 benchmark: str,
                 perses_root: Path,
                 jrts_root: Path,
                 custom_oracle: Path,
                 custom_input: Path) -> None:

        if benchmark and (custom_input or custom_input):
            raise Exception('Benchmarks and custom inputs for reduction are mutually exclusive. Use one of them.')

        self.tests = []

        if custom_input:
            self.tests.append((f'custom_{custom_input.stem}', ['custom', custom_oracle, custom_input]))
            return

        self.projects = {
            'jrts': jrts_root,
            'perses': perses_root,
        }

        if benchmark in BENCHMARKS:
            self.tests.append((benchmark, BENCHMARKS[benchmark]))
        else:
            self.tests += [(k, v) for k, v in BENCHMARKS.items() if k.startswith(benchmark)]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.tests):
            raise StopIteration

        name, (project, oracle, input_file) = self.tests[self.index]
        self.index += 1

        if project != 'custom':
            test_root = self.projects[project] / name
            oracle = test_root / oracle
            input_file = test_root / input_file

        if not oracle.is_file():
            raise Exception(f'Tester script for {name} does not exist ({oracle})')

        if not input_file.is_file():
            raise Exception(f'Input file for {name} does not exist ({input_file})')

        return name, oracle, input_file
