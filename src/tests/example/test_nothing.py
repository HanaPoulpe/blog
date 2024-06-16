"""
This is a sample test file
"""
import blog  # noqa
import pytest


class TestNothing:
    @pytest.mark.xfail
    def test_nothing(self) -> None:
        assert False
