import pytest
from leetcode import numIdenticalPairs, fillMissingValues, numSubarraysWithSum
import pandas as pd

def test_numIdenticalPairs():
    assert numIdenticalPairs([1, 2, 3, 1, 1, 3]) == 4
    assert numIdenticalPairs([1, 1, 1, 1]) == 6
    assert numIdenticalPairs([1, 2, 3]) == 0

def test_fillMissingValues():
    data = {
        'name': ['Wristwatch', 'WirelessEarbuds', 'GolfClubs', 'Printer'],
        'quantity': [None, None, 779, 849],
        'price': [135, 821, 9319, 3051]
    }
    df = pd.DataFrame(data)
    result = fillMissingValues(df)
    expected = pd.DataFrame({
        'name': ['Wristwatch', 'WirelessEarbuds', 'GolfClubs', 'Printer'],
        'quantity': [0, 0, 779, 849],
        'price': [135, 821, 9319, 3051]
    })
    pd.testing.assert_frame_equal(result, expected)

def test_numSubarraysWithSum():
    assert numSubarraysWithSum([1,0,1,0,1], 2) == 4
    assert numSubarraysWithSum([0,0,0,0,0], 0) == 15
    assert numSubarraysWithSum([1,1,1,1,1], 3) == 3

if __name__ == "__main__":
    pytest.main() 
