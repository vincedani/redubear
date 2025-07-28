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
    # 'jerry-3433': ['jrts', 'test.sh', '3433-orig.js'],
    'jerry-3437': ['jrts', 'test.sh', '3437-orig.js'],
    'jerry-3479': ['jrts', 'test.sh', '3479-orig.js'],
    # 'jerry-3483': ['jrts', 'test.sh', '3483-orig.js'],
    'jerry-3506': ['jrts', 'test.sh', '3506-orig.js'],
    'jerry-3523': ['jrts', 'test.sh', '3523-orig.js'],
    'jerry-3534': ['jrts', 'test.sh', '3534-orig.js'],
    # 'jerry-3536': ['jrts', 'test.sh', '3536-orig.js'],

    # Perses Test Suite (https://github.com/uw-pluverse/perses)
    # Note that the docker environment from the linked repository must be set up.
    # 'clang-18556': ['perses', 'r.sh', 'small.c'],
    'clang-18596': ['perses', 'r.sh', 'small.c'],
    # 'clang-19595': ['perses', 'r.sh', 'small.c'],
    # 'clang-20680': ['perses', 'r.sh', 'small.c'], # unstable
    # 'clang-21467': ['perses', 'r.sh', 'small.c'],
    'clang-21582': ['perses', 'r.sh', 'small.c'],
    'clang-22337': ['perses', 'r.sh', 'small.c'],
    # 'clang-22382': ['perses', 'r.sh', 'small.c'],
    'clang-22704': ['perses', 'r.sh', 'small.c'],
    'clang-23309': ['perses', 'r.sh', 'small.c'],
    # 'clang-23353': ['perses', 'r.sh', 'small.c'],
    'clang-25900': ['perses', 'r.sh', 'small.c'],
    'clang-26350': ['perses', 'r.sh', 'small.c'],
    # 'clang-26760': ['perses', 'r.sh', 'small.c'], # unstable
    'clang-27137': ['perses', 'r.sh', 'small.c'],
    'clang-27747': ['perses', 'r.sh', 'small.c'],
    'clang-31259': ['perses', 'r.sh', 'small.c'],


    # Perses Test Suite (https://github.com/uw-pluverse/perses)
    # Note that the docker environment from the linked repository must be set up.
    # 'gcc-58731': ['perses', 'r.sh', 'small.c'], # HDD: ANTLRv4 parse error: missing include directives -> PASS-es the test
    'gcc-59903': ['perses', 'r.sh', 'small.c'],
    # 'gcc-60116': ['perses', 'r.sh', 'small.c'], # unstable
    'gcc-60452': ['perses', 'r.sh', 'small.c'],
    # 'gcc-61047': ['perses', 'r.sh', 'small.c'], # unstable
    # 'gcc-61383': ['perses', 'r.sh', 'small.c'],
    'gcc-61917': ['perses', 'r.sh', 'small.c'],
    'gcc-64990': ['perses', 'r.sh', 'small.c'],
    'gcc-65383': ['perses', 'r.sh', 'small.c'],
    'gcc-66186': ['perses', 'r.sh', 'small.c'],
    'gcc-66375': ['perses', 'r.sh', 'small.c'],
    'gcc-66412': ['perses', 'r.sh', 'small.c'],
    # 'gcc-66691': ['perses', 'r.sh', 'small.c'],
    'gcc-70127': ['perses', 'r.sh', 'small.c'],
    'gcc-70586': ['perses', 'r.sh', 'small.c'],
    # 'gcc-71626': ['perses', 'r.sh', 'small.c'],


    # Perses Test Suite (https://github.com/uw-pluverse/perses)
    # Note that the docker environment from the linked repository must be set up.
    # 'xml/xml-071d221-1': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-071d221-2': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-1': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-2': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-3': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-4': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-1e9bc83-5': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-6': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-7': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-8': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-1e9bc83-9': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-2d4ec80-1': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-327c8af-1': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-3398ac2-1': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-3398ac2-2': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-3398ac2-3': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-3398ac2-4': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-3398ac2-5': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-4c99b96-1': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-4c99b96-2': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-3': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-4': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-5': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-6': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-7': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-8': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-9': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-4c99b96-10': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-11': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-4c99b96-12': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-13': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-14': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-15': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-16': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-17': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-4c99b96-18': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-4c99b96-19': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-1': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-2': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-8ede045-3': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-4': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-5': ['perses', 'r.sh', 'input.xml'],
    'xml/xml-8ede045-6': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-7': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-8ede045-8': ['perses', 'r.sh', 'input.xml'],
    # 'xml/xml-f053486-1': ['perses', 'r.sh', 'input.xml'],
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
                                      choices=['clang', 'gcc', 'jerry', 'xml', 'all', 'perses', 'debug'] + list(BENCHMARKS.keys()),
                                      default=None,
                                      help='Test case to be reduced. "jerry", "clang", "gcc": whole test suite. "perses": "clang" + "gcc"')

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
            if benchmark == 'all':
                benchmark = ['clang', 'gcc', 'xml', 'jerry']
            if benchmark == 'perses':
                benchmark = ['clang', 'gcc', 'xml']
            elif benchmark == 'debug':
                benchmark = ['gcc-71626', 'clang-22382', 'gcc-66691', 'clang-23353']
            else:
                benchmark = [benchmark]

            self.tests += [(k, v) for k, v in BENCHMARKS.items() if any(k for b in benchmark if k.startswith(b))]

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
