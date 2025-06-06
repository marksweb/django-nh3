#!/usr/bin/env python
from __future__ import annotations

import os
import subprocess
import sys
from functools import partial
from pathlib import Path

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    common_args = [
        "uv",
        "pip",
        "compile",
        "--quiet",
        "--generate-hashes",
        "--constraint",
        "-",
        "requirements.in",
        *sys.argv[1:],
    ]
    run = partial(subprocess.run, check=True)
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django32.txt",
        ],
        input=b"Django>=3.2a1,<3.3",
    )
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django40.txt",
        ],
        input=b"Django>=4.0a1,<4.1",
    )
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django41.txt",
        ],
        input=b"Django>=4.1a1,<4.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django42.txt",
        ],
        input=b"Django>=4.2a1,<5.0",
    )
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django50.txt",
        ],
        input=b"Django>=5.0a1,<5.1",
    )
    run(
        [
            *common_args,
            "--python",
            "3.10",
            "--output-file",
            "py310-django51.txt",
        ],
        input=b"Django>=5.1a1,<5.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.11",
            "--output-file",
            "py311-django41.txt",
        ],
        input=b"Django>=4.1a1,<4.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.11",
            "--output-file",
            "py311-django42.txt",
        ],
        input=b"Django>=4.2a1,<5.0",
    )
    run(
        [
            *common_args,
            "--python",
            "3.11",
            "--output-file",
            "py311-django50.txt",
        ],
        input=b"Django>=5.0a1,<5.1",
    )
    run(
        [
            *common_args,
            "--python",
            "3.11",
            "--output-file",
            "py311-django51.txt",
        ],
        input=b"Django>=5.1a1,<5.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.12",
            "--output-file",
            "py312-django42.txt",
        ],
        input=b"Django>=4.2a1,<5.0",
    )
    run(
        [
            *common_args,
            "--python",
            "3.12",
            "--output-file",
            "py312-django50.txt",
        ],
        input=b"Django>=5.0a1,<5.1",
    )
    run(
        [
            *common_args,
            "--python",
            "3.12",
            "--output-file",
            "py312-django51.txt",
        ],
        input=b"Django>=5.1a1,<5.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.12",
            "--output-file",
            "py312-django52.txt",
        ],
        input=b"Django>=5.2,<6.0",
    )
    run(
        [
            *common_args,
            "--python",
            "3.13",
            "--output-file",
            "py313-django51.txt",
        ],
        input=b"Django>=5.1a1,<5.2",
    )
    run(
        [
            *common_args,
            "--python",
            "3.13",
            "--output-file",
            "py313-django52.txt",
        ],
        input=b"Django>=5.2,<6.0",
    )
