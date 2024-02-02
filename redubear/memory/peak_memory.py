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

from redubear.utils import get_logger


class PeakMemory:
    def __init__(self, temp_dir: Path) -> None:
        self.root = Path(__file__).parent.resolve()
        self.temp_dir = temp_dir
        self.memory_file = self.temp_dir / 'peak_memory.txt'
        self.logger = get_logger('ReduBear')

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

        reducer_memory = peak_memory - sut_memory

        # Note: It might happen that the SUT consumes more memory than the reducer itself.
        # In that case, the 'time' command will give back the SUT peak memory as the reducer started that process.
        if reducer_memory == 0:
            self.logger.warning('The SUT consumed more memory than the reducer itself. The reported value is from the SUT!')
            return sut_memory

        if reducer_memory < 0:
            raise Exception('Something bad happened during memory calculation! Please debug it yourself!')

        return reducer_memory
