# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Miscellaneous utilities"""

from contextlib import contextmanager
import functools
import itertools
import logging
import operator
import os
import re
import sys
import time


def ensure_dir_exists(directory):
    "Creates local directories if they don't exist."
    if directory.startswith('gs://'):
        return
    print("Making dir {}".format(directory), file=sys.stderr)
    os.makedirs(directory, exist_ok=True)


def parse_game_result(result):
    "Parse an SGF result string into value target."
    if re.match(r'[bB]\+', result):
        return 1
    elif re.match(r'[wW]\+', result):
        return -1
    return 0


def product(iterable):
    "Like sum(), but with multiplication."
    return functools.reduce(operator.mul, iterable)


def _take_n(num_things, iterable):
    return list(itertools.islice(iterable, num_things))


def iter_chunks(chunk_size, iterator):
    "Yield from an iterator in chunks of chunk_size."
    iterator = iter(iterator)
    while True:
        next_chunk = _take_n(chunk_size, iterator)
        # If len(iterable) % chunk_size == 0, don't return an empty chunk.
        if next_chunk:
            yield next_chunk
        else:
            break


@contextmanager
def timer(message):
    "Context manager for timing snippets of code."
    tick = time.time()
    yield
    tock = time.time()
    print("%s: %.3f seconds" % (message, (tock - tick)))


@contextmanager
def logged_timer(message):
    "Context manager for timing snippets of code. Echos to logging module."
    tick = time.time()
    yield
    tock = time.time()
    print("%s: %.3f seconds" % (message, (tock - tick)))
    logging.info("%s: %.3f seconds", message, (tock - tick))
