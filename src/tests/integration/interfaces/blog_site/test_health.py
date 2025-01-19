from collections.abc import Callable

import pytest

from blog.application.queries import health


class TestHealthCheck:
    @pytest.mark.parametrize(
        "health_check",
        [health.is_alive, health.is_ready],
        ids=["liveness", "readiness"],
    )
    def test_is_healthy(self, health_check: Callable[[], bool]) -> None:
        assert health_check()

    @pytest.mark.parametrize(
        "health_check",
        [health.liveness_check, health.readiness_check],
        ids=["liveness", "readiness"],
    )
    def test_health_check(self, health_check: Callable[[], dict[str, str]]) -> None:
        assert all(map((lambda x: x == "working"), health_check().values()))
