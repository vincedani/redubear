# Copyright (c) 2024 Daniel Vince.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.md or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()

GRAMMARS = {
    'js':   ([ROOT_DIR / 'JavaScriptLexer.g4',
              ROOT_DIR / 'JavaScriptLexerBase.py',
              ROOT_DIR / 'JavaScriptParser.g4',
              ROOT_DIR / 'JavaScriptParserBase.py'],
             'program'),
    'c': ([ROOT_DIR / 'C.g4'], 'compilationUnit')
}


def get_grammar(extension: str):
    if extension not in GRAMMARS:
        raise Exception(f'The given input type ({extension}) is not supported.')

    grammar, start_rule = GRAMMARS[extension]
    grammar = [str(g) for g in grammar]

    return grammar, start_rule
