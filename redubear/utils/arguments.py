# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from pathlib import Path
from argparse import ArgumentParser

def process_path(parser: ArgumentParser, p: str, should_exist: bool = False) -> Path:
    path = Path(p).resolve()

    if should_exist and not path.exists():
        parser.error(f'{path} does not exist!')

    return path
