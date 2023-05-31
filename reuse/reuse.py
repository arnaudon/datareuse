"""Reuse saved dataset with contextmanager."""
from contextlib import contextmanager
from pathlib import Path

import pandas as pd


@contextmanager
def Reuse(filename, disable=False, **io_kwargs):
    """Context manager to reuse existing data file from previous run.

    At the moment, it is saved with pandas in .csv format only.

    index is passed to to_csv and index_col to read_csv

    Usage is as follow:

        with Reuse("data.csv") as reuse:
            df = reuse(computation, args, kwargs)
    """

    class reuse_data:
        """reuse class."""

        def __init__(self, filename):
            self._filename = filename
            self._io_kwargs = io_kwargs
            self._read = None
            self._write = None
            self.dispatch_io()

        def dispatch_io(self):
            """dispatch io"""
            if Path(self._filename).suffix == ".csv":

                def read():
                    return pd.read_csv(
                        self._filename, index_col=self._io_kwargs.get("index_col", None)
                    )

                def write(data):
                    data.to_csv(self._filename, index=self._io_kwargs.get("index", True))

            else:
                raise ValueError("File format not understood.")

            self._read = read
            self._write = write

        def __call__(self, computation, *args, **kwargs):
            """call method"""
            if not disable and Path(self._filename).exists():
                return self._read()

            data = computation(*args, **kwargs)

            self._write(data)
            return data

    yield reuse_data(filename)
