import enum
import functools

from health_check import mixins


class Check(enum.StrEnum):
    READY = "readiness"
    ALIVE = "liveness"


def _health_check(check: Check) -> dict[str, str]:
    checker = mixins.CheckMixin()
    checker.check(check.value)

    return {
        str(plugin_identifier): str(p.pretty_status())
        for plugin_identifier, p in checker.filter_plugins(check.value).items()
    }


def _is_check_healthy(check: Check) -> bool:
    checker = mixins.CheckMixin()
    return not checker.check(check.value)


readiness_check = functools.partial(_health_check, Check.READY)
is_ready = functools.partial(_is_check_healthy, Check.READY)
liveness_check = functools.partial(_health_check, Check.ALIVE)
is_alive = functools.partial(_is_check_healthy, Check.ALIVE)
