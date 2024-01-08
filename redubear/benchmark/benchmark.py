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
from shutil import copy2, rmtree

from redubear.benchmark import Tests
from redubear.memory import PeakMemory
from redubear.reducers import Reducer
from redubear.utils import get_logger, run_command, ReportGenerator


def run_single(name: str,
               reducer: Reducer,
               oracle: Path,
               input_file: Path,
               tag: str,
               memory: bool,
               output: Path,
               temp: Path,
               logger):
    # Note: "cannot pickle '_thread.lock' object" Exception occurs if this function is inside
    # the Benchmark class.
    logger.info(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {name} started ...')

    temporal_dir = temp / 'redubear' / name / tag
    final_out_dir = output / name / tag
    stat_file = final_out_dir / 'picire.json'

    makedirs(final_out_dir, exist_ok=True)
    makedirs(temporal_dir, exist_ok=True)

    command = []
    if memory:
        memory_measurer = PeakMemory(temporal_dir)
        command += memory_measurer.generate_command()

        oracle_wrapper = Path(temporal_dir / 'redubear-wrapper.py')
        oracle = memory_measurer.generate_oracle_wrapper(oracle, oracle_wrapper)

    command += reducer.generate_command(oracle, input_file, temporal_dir, stat_file)

    exit_code, stdout = run_command(
        command,
        oracle.parent,
        env=dict(environ, PYTHONOPTIMIZE='1'),
    )

    logger.info(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {name} exited with: {exit_code}')

    report = dict()
    if exit_code == 0:
        stats = ReportGenerator.read(stat_file)

        copy2(stats['path_output'], final_out_dir)
        stats['path_output'] = str(final_out_dir / input_file.name)

        stats['cache_size (kbytes)'] = round(stats['cache_size'] / 1024, 2)
        del stats['cache_size']

        if memory:
            stats['peak_memory (kbytes)'] = memory_measurer.get(stdout)

        ReportGenerator.dump(stats, stat_file)
        report[name] = stats
    else:
        logger.error(stdout)
        report[name] = {'error': exit_code}

    rmtree(temporal_dir)
    return report


class Benchmark:
    def __init__(self, inputs: Tests, reducer: Reducer, tag: str, workers: int, memory: bool, output: Path, temp: Path) -> None:
        self.inputs = inputs
        self.reducer = reducer
        self.tag = tag
        self.memory = memory
        self.output = output
        self.temp = temp

        self.executor = ProcessPoolExecutor(max_workers=workers)
        self.logger = get_logger('ReduBear')

    def run(self) -> dict:
        futures = []
        report = dict()

        start_time = time.time()
        for test_name, oracle, input_file in self.inputs:
            futures.append(self.executor.submit(
                run_single, test_name, self.reducer, oracle, input_file, self.tag, self.memory, self.output, self.temp, self.logger))

        # wait for all tasks to complete
        done, not_done = wait(futures, return_when=ALL_COMPLETED)

        for result in done:
            report.update(result.result())

        self.logger.info(
            f'Benchmark time: {timedelta(seconds=(time.time() - start_time))}')
        return report
