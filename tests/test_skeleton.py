# -*- coding: utf-8 -*-

import pytest

from fuel_price_tracker.skeleton import fib

__author__ = "Adrien Raison"
__copyright__ = "Adrien Raison"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
