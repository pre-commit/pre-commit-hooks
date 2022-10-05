from __future__ import annotations

import io
import re
import tokenize


def handle_match(token_text: str) -> str:
    if '"""' in token_text or "'''" in token_text:
        return token_text

    match = START_QUOTE_RE.match(token_text)
    if match is not None:
        meat = token_text[match.end():-1]
        if '"' in meat or "'" in meat:
            return token_text
        else:
            return match.group().replace('"', "'") + meat + "'"
    else:
        return token_text


def get_line_offsets_by_line_no(src: str) -> list[int]:
    # Padded so we can index with line number
    offsets = [-1, 0]
    for line in src.splitlines(True):
        offsets.append(offsets[-1] + len(line))
    return offsets


def fix_strings_in_file_contents(contents: str) -> str:
    line_offsets = get_line_offsets_by_line_no(contents)

    # Basically a mutable string
    splitcontents = list(contents)

    # Iterate in reverse so the offsets are always correct
    tokens_l = list(tokenize.generate_tokens(io.StringIO(contents).readline))
    tokens = reversed(tokens_l)
    for token_type, token_text, (srow, scol), (erow, ecol), _ in tokens:
        if token_type == tokenize.STRING:
            new_text = handle_match(token_text)
            splitcontents[
                line_offsets[srow] + scol:
                line_offsets[erow] + ecol
            ] = new_text

    new_contents = ''.join(splitcontents)
    return new_contents


START_QUOTE_RE = re.compile('^[a-zA-Z]*"')
