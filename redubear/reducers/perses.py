# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from pathlib import Path
from shutil import copy2

from redubear.reducers import Reducer
from redubear.utils import process_path
from redubear.utils import ReducerRegistry
from redubear.utils import run_command


@ReducerRegistry.register('perses')
class Perses(Reducer):

    @staticmethod
    def add_subparser(arg_parser) -> None:
        parser = arg_parser.add_parser(
            'perses', help='Arguments for Perses reducer')

        parser.add_argument('--jar', required=True,
                            type=lambda p: process_path(parser, p, should_exist=True),
                            help='The precompiled Perses jar file')

        parser.add_argument('--object-explorer', required=True,
                            type=lambda p: process_path(parser, p, should_exist=True),
                            help='The precompiled object explorer jar file')

        parser.add_argument('-j', '--jobs',
                            metavar='N',
                            type=int,
                            default=1,
                            help='maximum number of test commands to execute in parallel. default: %(default)s)')

        parser.add_argument('--cache',
                            metavar='NAME',
                            choices=['COMPACT_QUERY_CACHE', 'COMPACT_QUERY_CACHE_FORMAT_SENSITIVE',
                                     'CONFIG_BASED', 'CONTENT_LEXEME_LIST_BASE', 'CONTENT_SHA512',
                                     'CONTENT_SHA512_FORMAT', 'CONTENT_ZIP', 'ORIG_CONTENT_STRING_BASED',
                                     'PERSES_FAST_LINEAR_SCAN_NO_COMPRESSION', 'PERSES_LEXEME_ID', 'RCC_MEM_LIT' ],
                            default='COMPACT_QUERY_CACHE',
                            help='cache strategy (%(choices)s; default: %(default)s)')

    def __init__(self,
                 jar: Path,
                 object_explorer: Path,
                 cache: str,
                 jobs: int,
                 **kwargs) -> None:
        self.jar = jar
        self.object_explorer = object_explorer
        self.cache = cache
        self.jobs = jobs

    def generate_command(self, oracle: Path, input_file: Path, temp: Path, stats: Path) -> list[str]:
        command = [
            'java',
            f'-javaagent:{self.object_explorer}',
            '-jar', str(self.jar),
            '--verbosity', 'CONFIG',  # SEVERE, WARNING, INFO, CONFIG, FINE, FINER, FINEST
            '--query-caching', 'TRUE',  # TRUE, FALSE, AUTO
            '--code-format', 'ORIG_FORMAT',
            '--test-script', str(oracle),
            '--input-file', str(input_file),
            '--output-dir', str(temp),
            '--threads', str(self.jobs),  # positive integer or 'auto',
            '--stat-dump-file', str(stats),
            '--query-cache-type', self.cache,
            '--profile-query-cache-memory', str(stats.parent / f'{stats.stem}.pqcm'),
        ]

        # In one reduction process, only the "cache memory size" OR the "cache item count" can be
        # measured. Cannot do both at once. The "memory size" is prioritized higher.
        # '--profile-query-cache', str(stats.parent / f'{stats.stem}.pqc'),

        # Possible reduction algorithms:
        # '--alg'
        #    concurrent_state_ddmin
        #    ddmin
        #    hdd
        #    perses_node_priority_with_dfs_delta
        #    perses_node_with_bfs_delta
        #    perses_node_with_dfs_delta
        #    pristine_hdd

        return command

    def post_process(self, stat_file, input_file, out_dir, temp_dir) -> dict:
        # iteration before_size after_size removed_tokens time(ms) queries
        # total 149 42 107 12823 124
        with open(stat_file) as file:
            contents = file.readlines()

        stats = dict()
        for line in contents:
            if 'total' in line:
                parts = line.split()
                stats['runtime'] = round(float(parts[5]) / 1000., 2) # ms -> s
                stats['tests_started'] = int(parts[6])

            if 'iterations' in line:
                parts = line.split('=')
                stats['iterations'] = int(parts[-1])

        secondary_stat_file = stat_file.parent / f'testscript-{stat_file.name}'
        with open(secondary_stat_file) as file:
            contents = file.readlines()

        for line in contents:
            if 'pass_count' in line:
                parts = line.split('=')
                stats['tests_passed'] = int(parts[-1])

            if 'fail_count' in line:
                parts = line.split('=')
                stats['tests_failed'] = int(parts[-1])

        memory_stat_file = stat_file.parent / f'{stat_file.stem}.pqcm'
        with open(memory_stat_file) as file:
            contents = file.readlines()

        # timestamp cache_size (bytes)
        cache_size = max([int(line.split()[-1]) for line in contents])
        stats['cache_size (kbytes)'] = round(cache_size / 1024, 2)

        stats['path_input'] = str(input_file)

        reduced_file = temp_dir / input_file.name
        destination = out_dir / input_file.name
        copy2(reduced_file, destination)
        stats['path_output'] = str(destination)

        def measure_file(path):
            with open(path) as file:
                return sum(len(word) for line in file.readlines() for word in line.split())

        stats['bytes_input'] = input_file.stat().st_size
        stats['bytes_output'] = destination.stat().st_size

        stats['nws_input'] = measure_file(input_file)
        stats['nws_output'] = measure_file(destination)

        exit_code, stdout = run_command(
            ['java', '-jar', str(self.jar), '--version'],
            temp_dir.parent,
        )

        stats['reducer'] = 'perses-unknown'
        if exit_code == 0:
            version = 'perses'
            for line in stdout.splitlines():
                if 'perses version' in line:
                    version = f'{version}-{line.split()[-1]}'
                if 'Git Version' in line:
                    version = f'{version}-{line.split()[-1][:7]}'

            stats['reducer'] = version

        # Perses generates files as "input_file.timestamp.orig". Delete them.
        [p.unlink() for p in input_file.parent.glob(f'{input_file.stem}.*.orig')]

        return stats
