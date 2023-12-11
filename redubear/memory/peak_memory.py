# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
import stat

from os import chmod
from pathlib import Path
from string import Template

class PeakMemory:
    def __init__(self, temp_dir: Path) -> None:
        self.root = Path(__file__).parent.resolve()
        self.temp_dir = temp_dir
        self.memory_file = self.temp_dir / 'peak_memory.txt'

    def generate_command(self):
        return ['/usr/bin/time', '-f', '%M']

    def generate_oracle_wrapper(self, oracle: Path, target: Path) -> Path:

        with open(self.root / 'wrapper-template.txt', 'r') as template:
            source = Template(template.read())

        variables = {
            'oracle': oracle,
            'mem_lock': self.temp_dir / 'peak_memory.lock',
            'mem_file': self.memory_file,
        }

        result = source.safe_substitute(variables)

        with open(target, 'w+') as oracle:
            oracle.write(result)

        chmod(target, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)

        return target

    def get(self, stdout: str):
        peak_memory = int(stdout)

        with open(self.memory_file, 'r') as mem_file:
            data = mem_file.read()
            sut_memory = 0 if data == '' else int(data)

        return peak_memory - sut_memory
