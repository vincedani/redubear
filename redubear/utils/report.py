# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.
import json

from pathlib import Path

class ReportGenerator:
    @staticmethod
    def read(path: Path) -> dict:
        extension = path.suffix

        with open(path, 'r') as stat:
            if extension == '.json':
                return json.load(stat)
            else:
                raise NotImplementedError('Currently only JSON format is supported.')

    @staticmethod
    def dump(report: dict, path: Path) -> None:
        extension = path.suffix

        with open(path, 'w') as stat:
            if extension == '.json':
                 json.dump(report, stat, indent=4, sort_keys=True)
            else:
                raise NotImplementedError('Currently only JSON format is supported.')
