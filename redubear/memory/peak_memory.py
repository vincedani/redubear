# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
from pathlib import Path

from redubear.utils import get_logger, run_command


class PeakMemory:
    def __init__(self, temp_dir: Path) -> None:
        self.temp_dir = temp_dir
        self.memory_file = self.temp_dir / 'valgrind.out'
        self.logger = get_logger('ReduBear')

    def generate_command(self):
        return [
            'valgrind',
            '--tool=massif',
            '--stacks=yes',
            '--trace-children=no',
            '--pages-as-heap=no',
            '--quiet',
            f'--massif-out-file={self.memory_file}'
        ]

    def get(self):
        command = ['ms_print', str(self.memory_file)]
        exit_code, stdout = run_command(command, self.memory_file.parent)

        if exit_code:
            self.logger.error(stdout)
            return -1

        peak_memory = stdout.splitlines()[8]
        peak_memory = peak_memory.partition('^')[0]

        return float(peak_memory)
