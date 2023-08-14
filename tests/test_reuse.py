import pandas as pd
from pathlib import Path
import pytest

from datareuse import Reuse


DATA = Path(__file__).parent


def test_reuse(tmpdir):
    """Test reuse context manager."""

    def comp(fact=1.0):
        df = pd.DataFrame(index=[0, 1, 2], columns=["a", "b", "c"], dtype=float)
        df.loc[0] = [1, 2, 3 * fact]
        df.loc[1] = [2, 3 * fact, 4]
        df.loc[2] = [3 * fact, 4, 5]
        return df

    with Reuse(tmpdir / "data_1.csv", index_col=0) as reuse:
        df1 = reuse(comp)

    with Reuse(DATA / "data.csv", index_col=0) as reuse:
        df2 = reuse(comp)

    assert df1.equals(df2)

    with Reuse(DATA / "data.csv", index_col=0, disable=True) as reuse:
        df3 = reuse(comp)

    assert df1.equals(df3)

    with Reuse(tmpdir / "data_2.csv", index=False, disable=True) as reuse:
        df4 = reuse(comp)

    assert df1.equals(df4)

    with pytest.raises(ValueError):
        with Reuse(tmpdir / "data.unknown", index_col=0, disable=True) as reuse:
            reuse(comp)

    with Reuse(tmpdir / "data_3.csv", index=False) as reuse:
        df5 = reuse(comp, 2)
    assert not df1.equals(df5)

    with Reuse(tmpdir / "data_4.csv", index=False) as reuse:
        df6 = reuse(comp, 2)

    assert df5.equals(df6)

    # test yaml
    def create_dict():
        return {"a": 123, "b": [1, 2, 3]}

    with Reuse(tmpdir / "data.yaml") as reuse:
        data_orig = reuse(create_dict)

    with Reuse(DATA / "data.yaml") as reuse:
        data_reuse = reuse(create_dict)
    assert data_orig == data_reuse
