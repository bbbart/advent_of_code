#!/usr/bin/env python

"""Convenience wrapper to run code for the Advent of Code challenges."""

import contextlib
import sys
from copy import deepcopy
from datetime import datetime
from importlib import import_module
from pathlib import Path

try:
    DAY = sys.argv[1].zfill(2)
except IndexError:
    sys.exit("Which day?")

try:
    YEAR = sys.argv[2]
except IndexError:
    YEAR = str(datetime.now().year)

try:
    answer_code = import_module(f"{YEAR}.day_{DAY}.answer")
except ModuleNotFoundError:
    sys.exit(f"No answer found for day {DAY} {YEAR}!")

data_path = Path(".") / YEAR / f"day_{DAY}"
data_samp_fp = data_path / "input_sample"
data_real_fp = data_path / "input"

results = {}
print("RUNNING:")
for part in 1, 2:
    for dataset in ("samp", "real"):
        data_fp = locals()[f"data_{dataset}_fp"]
        if data_fp.exists():
            data = data_fp.read_text(encoding="utf-8").splitlines()
            results_key = f"part {part}, {dataset} data"
            with contextlib.suppress(AttributeError):
                print(results_key, end=' ')
                try:
                    result = getattr(answer_code, f"p{part}")(
                        deepcopy(data), is_sample=dataset == "samp"
                    )
                    results[results_key] = result
                    print("[\033[92mOK\033[0m]", result)
                except Exception as err:
                    print("[\033[91mNOK\033[0m]", str(err))
                    raise err

print()
print("RESULTS:")
for key, result in results.items():
    print(f"{key}: {result}")
