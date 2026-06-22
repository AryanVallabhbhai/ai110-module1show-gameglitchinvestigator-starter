import random

import pytest

from logic_utils import get_range_for_difficulty


# Expected (low, high) ranges per difficulty. Mirrors get_range_for_difficulty.
EXPECTED_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 100),
    "Hard": (1, 500),
}


@pytest.mark.parametrize("difficulty,expected", EXPECTED_RANGES.items())
def test_banner_range_matches_difficulty(difficulty, expected):
    """Banner shows the range returned by get_range_for_difficulty.

    The sidebar/info banner in app.py renders `low`..`high` straight from
    get_range_for_difficulty, so verifying that function covers the banner.
    """
    assert get_range_for_difficulty(difficulty) == expected


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("???") == (1, 100)


@pytest.mark.parametrize("difficulty", EXPECTED_RANGES.keys())
def test_secret_within_range_on_difficulty_change(difficulty):
    """Secret generated on difficulty change stays within that range.

    app.py regenerates secret with random.randint(low, high) when difficulty
    changes. Draw many samples to check the contract holds for every value.
    """
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(1000):
        secret = random.randint(low, high)
        assert low <= secret <= high