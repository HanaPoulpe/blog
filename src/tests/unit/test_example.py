import pytest


class TestNothing:
    @pytest.mark.xfail
    def test_nothing(self) -> None:
        raise NotImplementedError()
