# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from os import environ

from redubear.utils import get_logger
from subprocess import Popen, PIPE


def run_command(command, cwd, env=environ):
    logger = get_logger('ReduBear')
    logger.debug(f'Running: {" ".join(command)}')

    process = Popen(command,
                    cwd=cwd.resolve(),
                    env=env,
                    stdout=PIPE,
                    stderr=PIPE)
    out, err = process.communicate()

    stdout = str(out, encoding='utf-8')
    stderr = str(err, encoding='utf-8')
    return process.returncode, f'{stdout} {stderr}'
