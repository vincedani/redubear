# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import time

from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
from datetime import datetime, timedelta
from os import environ, makedirs
from pathlib import Path
from shutil import rmtree

from redubear.benchmark import Tests
from redubear.memory import PeakMemory
from redubear.reducers import Reducer
from redubear.utils import get_logger, run_command, ReportGenerator


def run_single(name: str,
               reducer: Reducer,
               oracle: Path,
               input_file: Path,
               tag: str,
               valgrind: bool,
               output: Path,
               temp: Path,
               force: bool,
               logger):
    # Note: "cannot pickle '_thread.lock' object" Exception occurs if this function is inside
    # the Benchmark class.
    temporal_dir = temp / 'redubear' / name / tag
    final_out_dir = output / name / tag
    stat_file = final_out_dir / 'picire.json'

    report = dict()

    if not force:
        reduced_file = final_out_dir / input_file.name
        # Both statistics and the reduced file exist, returning the results of the
        # previous experiment.
        if stat_file.exists() and reduced_file.exists():
            pervious_results = ReportGenerator.read(stat_file)
            logger.info(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {name} load cached results')
            report[name] = pervious_results
            return report

    logger.info(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {name} started ...')

    makedirs(final_out_dir, exist_ok=True)
    makedirs(temporal_dir, exist_ok=True)

    command = []
    if valgrind:
        memory_measurer = PeakMemory(temporal_dir)
        command += memory_measurer.generate_command()

    command += reducer.generate_command(oracle, input_file, temporal_dir, stat_file)

    exit_code, stdout = run_command(
        command,
        oracle.parent,
        env=dict(environ, PYTHONOPTIMIZE='1', PERSES_CACHE_MEMORY_PROFILING_TIME_INTERVAL='3000'),
    )

    logger.info(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {name} exited with: {exit_code}')

    if exit_code == 0:
        stats = reducer.post_process(stat_file, input_file, final_out_dir, temporal_dir)

        if valgrind:
            stats['peak_memory (MB)'] = memory_measurer.get()

        ReportGenerator.dump(stats, stat_file)
        report[name] = stats
    else:
        logger.error(stdout)
        report[name] = {'error': exit_code}

    rmtree(temporal_dir)
    return report


class Benchmark:
    def __init__(self,
                 inputs: Tests,
                 reducer: Reducer,
                 tag: str,
                 workers: int,
                 valgrind: bool,
                 output: Path,
                 temp: Path,
                 force: bool) -> None:
        self.inputs = inputs
        self.reducer = reducer
        self.tag = tag
        self.valgrind = valgrind
        self.output = output
        self.temp = temp
        self.force = force

        self.executor = ProcessPoolExecutor(max_workers=workers)
        self.logger = get_logger('ReduBear')

    def run(self) -> dict:
        futures = []
        report = dict()

        start_time = time.time()
        for test_name, oracle, input_file in self.inputs:
            futures.append(self.executor.submit(
                run_single, test_name, self.reducer, oracle, input_file, self.tag, self.valgrind, self.output, self.temp, self.force, self.logger))

        # wait for all tasks to complete
        done, not_done = wait(futures, return_when=ALL_COMPLETED)

        for result in done:
            report.update(result.result())

        self.logger.info(
            f'Benchmark time: {timedelta(seconds=(time.time() - start_time))}')
        return report
