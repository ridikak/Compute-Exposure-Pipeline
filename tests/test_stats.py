import pandas as pd

def test_zscore_basic():
    x = pd.Series([1,2,3,4,5], dtype=float)
    mu = x.mean()
    sigma = x.std(ddof=1)
    z3 = (3 - mu) / sigma
    assert abs(z3) < 1
